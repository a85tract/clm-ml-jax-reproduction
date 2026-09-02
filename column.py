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
parser.add_argument("--dumps", default=str(HERE / "output/recorded/dumps/fortran_mlcanopyfluxesmod"))
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


first = load_step(1)
carried_names = {n for n in (a["name"].lower() for a in sig["args"] if a["intent"] != "OUT") if n in first["outputs"]}
# ncan is written inside step 1 (initVerticalStructure); step 2's input has it.
ncan = int(np.asarray(load_step(min(2, args.steps))["inputs"]["mlcanopy_inst__ncan_canopy"])[0])
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
print(f"mode={args.mode}  steps={args.steps}  carried={len(carried_names)}  exogenous={len(taken) - len(carried_names)}")
worst_of_day = (0.0, 0.0, "")
for k in range(1, args.steps + 1):
    sample = first if k == 1 else load_step(k)
    kw = {}
    for name in taken:
        low = name.lower()
        # np values go in as they are: traced positions accept them and the
        # static scalar positions NEED hashable np scalars, not jax arrays.
        kw[name] = state[low] if (low in state and k > 1) else sample["inputs"][low]
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
    if k in (1, 2, 6, 12, 24, 48) or step_rel > 1e-3:
        print(f"  step {k:3d}: max_abs {step_abs:.3e}  max_rel {step_rel:.3e}  ({step_name})")
print(f"worst of day: max_rel {worst_of_day[1]:.3e} at {worst_of_day[2]} (abs {worst_of_day[0]:.3e})")
