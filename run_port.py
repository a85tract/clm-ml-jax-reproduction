#!/usr/bin/env python3
"""Port every recorded unit to JAX and gate it on its recording.

    python run_port.py [unit ...]

For each ``output/recorded/<unit>.json`` (or the units named), runs the
``port-clm-ml`` recipe with the same recording the NumPy translation was held
bit-exact against, and writes ``output/port/summary.json``: per unit the
verdict, which subprograms became JAX kernels, and why the rest did not.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
# Scalars the JAX backend would make static arguments of the kernel (so it
# recompiles whenever they change) but which change every step: the per-step
# counter itim in the whole-step kernel. Kept traced, the month runs on one
# compile (REPRODUCTION.md, "Reverse mode through the whole step").
TRACED_SCALARS = {"fortran:mlcanopyfluxesmod": ["clm_time_manager__itim"]}

parser = argparse.ArgumentParser()
parser.add_argument("units", nargs="*")
parser.add_argument(
    "--recorded",
    default=str(OUT / "recorded"),
    help="the recording to gate on (output/recorded is day 1; output/recorded.day15 is "
    "day 15, which every kernel gate runs as well)",
)
parser.add_argument("--port", default=None, help="where the ports and summary go (default output/port, or output/port.<suffix of --recorded>)")
args = parser.parse_args()
RECORDED = Path(args.recorded).resolve()
suffix = RECORDED.name[len("recorded") :]  # "" or ".day15"
PORT = Path(args.port).resolve() if args.port else OUT / f"port{suffix}"
PORT.mkdir(exist_ok=True)
wanted = args.units
configs = sorted(RECORDED.glob("fortran_*.json"))
if wanted:
    configs = [c for c in configs if c.stem in {w.replace(":", "_") for w in wanted}]
# The summary is per recording and merged by unit: a run of one unit
# updates its row and leaves the others, so a whole-step run no longer
# erases the fifteen physics verdicts (it did once, 2026-09-02).
summary_path = PORT / "summary.json"
summary: dict[str, dict] = json.loads(summary_path.read_text()) if summary_path.is_file() else {}
for path in configs:
    uid = path.stem.replace("fortran_", "fortran:")
    config = json.loads(path.read_text())
    stages = config.setdefault("stages", {})
    if "translate.clm-ml" in stages:
        stages["port.clm-ml-jax"] = stages.pop("translate.clm-ml")
    if uid in TRACED_SCALARS:
        stages.setdefault("port.clm-ml-jax", {})["traced_scalars"] = TRACED_SCALARS[uid]
    config["output"] = str(PORT.relative_to(HERE))
    config["stages"]["dump-replay"]["dumps"] = str(
        (RECORDED / "dumps" / path.stem).relative_to(HERE)
    )
    (PORT / path.name).write_text(json.dumps(config, indent=2))
    run = subprocess.run(
        ["recast", "run", "port-clm-ml", "output/staged", "--config", str((PORT / path.name).relative_to(HERE)), "--unit", uid],
        cwd=HERE,  # the configs name paths relative to this directory
        capture_output=True,
        text=True,
    )
    text = run.stdout + run.stderr
    verdict = next((ln.strip() for ln in text.splitlines() if "differential.tolerance" in ln), "")
    stopped = next((ln.strip() for ln in text.splitlines() if "[!!]" in ln or "stopped" in ln), "")
    notes: dict = {}
    candidate = PORT / "port-clm-ml" / path.stem / "candidate"
    jax_file = candidate / f"{path.stem.replace('fortran_', '')}_jax.py"
    kernels: list[str] = []
    if jax_file.is_file():
        for line in jax_file.read_text().splitlines():
            if line.startswith("_JAX_KERNELS = "):
                kernels = json.loads(line.split("=", 1)[1].strip().replace("'", '"'))
    summary[uid] = {"verdict": verdict, "stopped": stopped, "kernels": kernels}
    print(f"{uid}: {verdict or stopped or text[-300:]}\n    kernels={kernels}")
summary_path.write_text(json.dumps(dict(sorted(summary.items())), indent=2) + "\n")
