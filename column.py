#!/usr/bin/env python3
"""Closed-loop column run: the whole-step kernel driven by its own outputs.

    python column.py [--mode numpy|jax] [--steps N] [--dumps DIR]

State that the recording shows carried (input at step k == output at step
k-1; 262 of the 456 inputs) comes from the previous step's own outputs;
the 194 exogenous inputs (tower forcing, CLM-side per-step fields,
t_soisno) come from the recording. Per step, every output is compared to
the recorded one: --mode numpy must be bit-exact (the composition is the
claim), --mode jax shows how the fusion-tier residual compounds over the
day -- the whole-column parity signal of the paper's Fig. 5.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np

from recast.oracle.dump_replay import parse_dump
from recast.verify.bitexact import BitexactVerifier

HERE = Path(__file__).resolve().parent

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=("numpy", "jax"), default="numpy")
parser.add_argument("--steps", type=int, default=48)
parser.add_argument(
    "--start",
    type=int,
    default=1,
    help="first model step (day 15 starts at 673; needs a recording that holds it, "
    "e.g. --dumps output/recorded.31day/dumps/fortran_mlcanopyfluxesmod)",
)
parser.add_argument("--dumps", default=str(HERE / "output/recorded/dumps/fortran_mlcanopyfluxesmod"))
parser.add_argument(
    "--bar",
    type=float,
    default=1e-3,
    help="the gate: max relative error over the run on each canopy flux "
    "(gppveg, lhflx, shflx, ustar). Exit 1 above it. The kernel regression of "
    "2026-08-31 read 13%% here; the fixed kernel 3e-5 (root-finder staircase).",
)
parser.add_argument(
    "--open-loop",
    action="store_true",
    help="feed every step the recorded inputs instead of the kernel's own outputs: "
    "the per-step kernel check, not the column; what the day-15 gate runs",
)
args = parser.parse_args()

cand = HERE / "output/port/port-clm-ml/fortran_mlcanopyfluxesmod/candidate"
sys.path.insert(0, str(cand))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, cand / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


host = load("mlcanopyfluxesmod_numpy")
module = host if args.mode == "numpy" else load("mlcanopyfluxesmod_jax")
fn = module.mlcanopyfluxes_flat
signatures = (host if args.mode == "numpy" else module)._SIGNATURES
sig = signatures["mlcanopyfluxes_flat"]
taken = [a["name"] for a in sig["args"] if a["intent"] != "OUT"]
outs = [a["name"] for a in sig["args"] if a["intent"] in ("OUT", "INOUT")]

dumps = Path(args.dumps)


def load_step(k: int) -> dict:
    npz = dumps / f"mlcanopyfluxes_flat_{k:04d}.npz"
    if npz.exists():
        with np.load(npz) as bundle:
            ins = {n[4:]: bundle[n] for n in bundle.files if n.startswith("in__")}
            recorded = {n[5:]: bundle[n] for n in bundle.files if n.startswith("out__")}
        sample = {"subprogram": "mlcanopyfluxes_flat", "inputs": ins, "outputs": recorded}
        # The same scalar typing the text path gets: a 0-d array in a static
        # argnum slot is unhashable.
        BitexactVerifier._type_recorded(np, [sample], signatures)
        return sample
    ins, recorded = parse_dump((dumps / f"mlcanopyfluxes_flat_{k:04d}.txt").read_text())
    sample = {"subprogram": "mlcanopyfluxes_flat", "inputs": ins, "outputs": recorded}
    BitexactVerifier._type_recorded(np, [sample], signatures)
    return sample


first = load_step(args.start)
carried_names = {n for n in (a["name"].lower() for a in sig["args"] if a["intent"] != "OUT") if n in first["outputs"]}
# ncan is written inside step 1 (initVerticalStructure); step 2's input has it.
ncan = int(np.asarray(load_step(min(args.start + 1, args.start + args.steps - 1))["inputs"]["mlcanopy_inst__ncan_canopy"])[0])
print(f"ncan = {ncan}")


def dominant(name: str, got: np.ndarray, want: np.ndarray):
    """The physically-meaningful entries: canopy arrays cut at ncan (the
    layer axis is 100, interfaces 101); everything else whole."""
    if got.ndim >= 2 and got.shape[1] == 100:
        return got[:, :ncan], want[:, :ncan]
    if got.ndim >= 2 and got.shape[1] == 101:
        return got[:, : ncan + 1], want[:, : ncan + 1]
    return got, want
state: dict[str, np.ndarray] = {}
loop = "open loop (recorded inputs every step)" if args.open_loop else "closed loop"
print(f"mode={args.mode}  {loop}  start={args.start}  steps={args.steps}  carried={len(carried_names)}  exogenous={len(taken) - len(carried_names)}")
worst_of_day = (0.0, 0.0, "")
FLUXES = ("gppveg_canopy", "lhflx_canopy", "shflx_canopy", "ustar_canopy")
flux_err: dict[str, list[float]] = {f: [] for f in FLUXES}
for k in range(args.start, args.start + args.steps):
    sample = first if k == args.start else load_step(k)
    kw = {}
    for name in taken:
        low = name.lower()
        # np values go in as they are: traced positions accept them and the
        # static scalar positions NEED hashable np scalars, not jax arrays.
        carry = low in state and k > args.start and not args.open_loop
        kw[name] = state[low] if carry else sample["inputs"][low]
    result = fn(**kw)
    result = result if isinstance(result, tuple) else (result,)
    step_abs = step_rel = 0.0
    step_name = ""
    for name, got in zip(outs, result):
        low = name.lower()
        got = np.asarray(got)
        if low in carried_names:
            state[low] = got
        want = sample["outputs"].get(low)
        if want is None or got.dtype.kind not in "fiu":
            continue
        want = np.asarray(want)
        gd, wd = dominant(low, got.astype(np.float64), np.asarray(want).astype(np.float64))
        for flux in FLUXES:
            if low.endswith(flux):
                denom = max(float(np.abs(wd).max()), 1e-12)
                flux_err[flux].append(float(np.abs(gd - wd).max()) / denom)
        diff = np.abs(gd - wd)
        # The array's own scale as the floor: a -2e-16 beside an exact 0 in
        # a mumol-scale array is not a relative error of 2e14.
        scale = max(float(np.abs(wd).max()) if wd.size else 0.0, 1e-30)
        rel = float(diff.max() / scale) if diff.size else 0.0
        if float(diff.max() if diff.size else 0.0) > step_abs:
            step_abs = float(diff.max())
        if rel > step_rel:
            step_rel, step_name = rel, low
    if step_rel > worst_of_day[1]:
        worst_of_day = (step_abs, step_rel, f"step {k}: {step_name}")
    if (k - args.start + 1) in (1, 2, 6, 12, 24, 48) or step_rel > 1e-3:
        print(f"  step {k:3d}: max_abs {step_abs:.3e}  max_rel {step_rel:.3e}  ({step_name})")
print(f"worst of day: max_rel {worst_of_day[1]:.3e} at {worst_of_day[2]} (abs {worst_of_day[0]:.3e})")
# The gate reads the canopy fluxes, per step, over the run: a leaf whose
# root finder took the other branch is a 100% error in that leaf and a
# staircase step in the total, and the total is what the paper's Fig. 5
# compares.
print(f"per-flux relative error over {args.steps} steps from step {args.start} (gate: max < {args.bar:g}):")
failed = False
for flux, errs in flux_err.items():
    if not errs:
        print(f"  {flux:16s} not in the outputs")
        failed = True
        continue
    e = np.array(errs)
    verdict = "ok" if e.max() < args.bar else "FAIL"
    failed = failed or verdict == "FAIL"
    print(f"  {flux:16s} median {np.median(e):.3e}  p95 {np.percentile(e, 95):.3e}  max {e.max():.3e}  {verdict}")
sys.exit(1 if failed else 0)
