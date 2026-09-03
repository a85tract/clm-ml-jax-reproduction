#!/usr/bin/env python3
"""Record flat-adapter inputs/outputs for CLM-ml units from a real run (Phase 3).

    python record.py fortran:mlleaffluxesmod fortran:mlsoilfluxesmod [--days 1] [--calls 40]

Generates the recorder module and a probed copy of the staged tree under
output/recorded/, builds it with gfortran the way build/build.sh builds the
reference, runs the CHATS7 May-2007 namelist for --days days, and sorts the
dumps into output/recorded/dumps/<unit>/. Then, per unit:

    recast run translate-clm-ml output/staged --config output/recorded/<unit>.json --unit <unit>
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from recast.registry import REGISTRY

from recast.oracle.record import RECORDER_MODULE, plans_for_units, probe_tree, recorder_module

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
STAGED = OUT / "staged"

parser = argparse.ArgumentParser()
parser.add_argument("units", nargs="+")
parser.add_argument("--days", type=int, default=1)
parser.add_argument("--calls", type=int, default=40)
parser.add_argument(
    "--start-step",
    type=int,
    default=1,
    help="record from this model step (48 per day; day 15 starts at 673). "
    "Every kernel gate runs day 15 beside day 1: day 1 is leaf-out and hid "
    "a real kernel regression (REPRODUCTION.md, 2026-08-31).",
)
parser.add_argument(
    "--out",
    default=None,
    help="recording directory (default output/recorded, or output/recorded.day<N> "
    "when --start-step is not 1). Never the directory of another recording: "
    "the dumps there are cleared.",
)
args = parser.parse_args()
if args.start_step > 1:
    args.days = max(args.days, -(-args.start_step // 48))
REC = (
    Path(args.out).resolve()
    if args.out
    else OUT / ("recorded" if args.start_step == 1 else f"recorded.day{-(-args.start_step // 48)}")
)

frontend = REGISTRY.get("frontend", "clm-ml")()
units = {u.uid: u for u in frontend.discover(STAGED)}
facts_by_module = {}
for uid in args.units:
    facts = frontend.analyze(units[uid], STAGED)
    facts_by_module[facts.interface["module"]] = facts
plans_by_module = plans_for_units(facts_by_module)
for module, plans in plans_by_module.items():
    print(f"{module}: adapters for {[p.subprogram['name'] for p in plans]}")

probed = REC / "staged"
sites = probe_tree(STAGED, probed, plans_by_module)
print("probed call sites:", sites)
# One recorder module for all units: merge by concatenating would define the
# module several times, so generate one module over all plans instead.
all_plans = [p for plans in plans_by_module.values() for p in plans]
window = None if args.start_step == 1 else ("clm_time_manager", "itim", args.start_step, 10**9)
recorder = recorder_module("recorder", all_plans, calls=args.calls, window=window)
# each probe line names its own module in the PROBE header
for module, plans in plans_by_module.items():
    for p in plans:
        recorder = recorder.replace(
            f"# PROBE recorder.{p.subprogram['name']}_flat", f"# PROBE {module}.{p.subprogram['name']}_flat"
        )
(probed / f"{RECORDER_MODULE}.f90").write_text(recorder)

# Build order: a topological sort over the probed tree's own USE statements,
# the recorder included -- it uses the type and state modules, and the probed
# callers use it, so a fixed order from before cannot place it.
import collections

by_stem = {p.stem.lower(): p for p in probed.glob("*.f90")}
module_of = {}
uses_of = {}
for stem, path in by_stem.items():
    text = path.read_text(errors="replace")
    m = re.search(r"^\s*(?:module|program)\s+(\w+)", text, re.I | re.M)
    if not m:
        continue
    module_of[m.group(1).lower()] = stem
    uses_of[m.group(1).lower()] = {u.lower() for u in re.findall(r"^\s*use\s+(\w+)", text, re.I | re.M)}
indeg = {m: 0 for m in module_of}
rev = collections.defaultdict(set)
for m, uses in uses_of.items():
    for u in uses:
        if u in module_of and u != m:
            indeg[m] += 1
            rev[u].add(m)
ready = sorted(m for m, d in indeg.items() if d == 0)
order = []
while ready:
    m = ready.pop(0)
    order.append(by_stem[module_of[m]].stem)
    for n in sorted(rev[m]):
        indeg[n] -= 1
        if indeg[n] == 0:
            ready.append(n)
    ready.sort()
if len(order) != len(module_of):
    raise SystemExit("the probed tree's USE graph has a cycle")
build = REC / "build"
if build.exists():
    shutil.rmtree(build)
(build / "obj").mkdir(parents=True)
nf = subprocess.run(["nf-config", "--prefix"], capture_output=True, text=True, check=True).stdout.strip()
nc_lib = subprocess.run(["nc-config", "--libdir"], capture_output=True, text=True, check=True).stdout.strip()
# The engine's reference build rounds this way (recast.oracle.f2py.DEFAULT_FLAGS);
# a recording made under -O2 differs from it by FMA contraction, a few ULP.
flags = [
    "-O1",
    "-fno-fast-math",
    "-ffp-contract=off",
    "-ffree-line-length-none",
    "-fno-range-check",
    f"-I{nf}/include",
]
objects = []
for name in order:
    src = by_stem.get(name.lower())
    if src is None:
        raise SystemExit(f"no source for {name}")
    obj = build / "obj" / f"{name}.o"
    subprocess.run(["gfortran", *flags, "-c", "-J", str(build / "obj"), "-o", str(obj), str(src)], check=True)
    objects.append(str(obj))
subprocess.run(
    ["gfortran", "-o", str(build / "prgm.exe"), *objects, f"-L{nf}/lib", "-lnetcdff", f"-L{nc_lib}", "-lnetcdf"],
    check=True,
)
print("built", build / "prgm.exe")

# Run from a directory laid out the way the model expects.
run = REC / "run"
if run.exists():
    shutil.rmtree(run)
(run / "out").mkdir(parents=True)
(run / "dumps").mkdir()
(REC / "rsl_lookup_tables").unlink(missing_ok=True)
(REC / "rsl_lookup_tables").symlink_to(HERE / "upstream" / "rsl_lookup_tables")
namelist = (HERE / "upstream" / "offline_executable" / "nl.CHATS7.05.2007").read_text()
namelist = re.sub(r"stop_n\s*=\s*\d+", f"stop_n           = {args.days}", namelist)
namelist = namelist.replace("'../input_files", f"'{HERE}/upstream/input_files").replace(
    "dirout           = '../output_files/'", "dirout           = './out/'"
)
(run / "nl").write_text(namelist)
with open(run / "run.log", "w") as log:
    subprocess.run([str(build / "prgm.exe")], stdin=open(run / "nl"), stdout=log, stderr=subprocess.STDOUT, cwd=run, check=True)
print("ran; last line:", (run / "run.log").read_text().strip().splitlines()[-1])

# The namelist's scalar settings, for the translation's constants.
overrides = {}
for key, raw in re.findall(r"^\s*(\w+)\s*=\s*([^'\n]+?)\s*$", namelist, re.M):
    token = raw.strip().replace("D0", "").replace("d0", "")
    try:
        overrides[key.lower()] = int(token) if re.fullmatch(r"-?\d+", token) else float(token)
    except ValueError:
        pass
overrides = {k: v for k, v in overrides.items() if k in {"met_type", "dpai_min", "pftcon_val"}}
print("constant overrides from the namelist:", overrides)

# Sort dumps per unit and write a config per unit.
dumps = REC / "dumps"
if dumps.exists():
    shutil.rmtree(dumps)
for module, plans in plans_by_module.items():
    uid = f"fortran:{module}"
    target = dumps / uid.replace(":", "_")
    target.mkdir(parents=True)
    n = 0
    for p in plans:
        for f in sorted((run / "dumps").glob(f"{p.subprogram['name']}_flat_*.txt")):
            shutil.copy2(f, target / f.name)
            n += 1
    config = {
        "output": str(OUT.relative_to(HERE)),
        "oracle": "dump-replay",
        "stages": {
            "dump-replay": {"dumps": str(target.relative_to(HERE))},
            # The run-control variables the namelist set: the tree's defaults
            # are what the translation would otherwise carry.
            "translate.clm-ml": {"constant_overrides": overrides},
        },
    }
    (REC / f"{uid.replace(':', '_')}.json").write_text(json.dumps(config, indent=2) + "\n")
    print(f"{uid}: {n} dump(s) -> {target}")
(REC / "RECORDING.md").write_text(
    "Recorded with gfortran "
    + subprocess.run(["gfortran", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    + f"\nflags: {' '.join(flags)}\nnamelist: nl.CHATS7.05.2007 with stop_n = {args.days}\n"
    f"calls per probe: {args.calls}\nrecorded from model step: {args.start_step}\n"
    f"probed sites: {sites}\n"
)
