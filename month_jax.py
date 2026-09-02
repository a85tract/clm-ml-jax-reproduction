#!/usr/bin/env python3
"""31-day closed-loop JAX run vs the Fortran recording: Fig-5 parity.

    python month_jax.py [--steps 1488] [--out output/trajectory.npy]

Carries the whole-step kernel's own outputs step to step (recorded inputs
only for the exogenous forcing), tracks headline fields against the
recording with dominant-region masking and per-array scale, saves the
per-step trajectory, and reports daily-mean relative drift per field --
the paper's Fig-5 criterion is 1%.
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
parser.add_argument("--steps", type=int, default=1488)
parser.add_argument("--dumps", default=str(HERE / "output/recorded.31day/dumps/fortran_mlcanopyfluxesmod"))
parser.add_argument("--out", default=str(HERE / "output/trajectory.npy"))
args = parser.parse_args()

cand = HERE / "output/port/port-clm-ml/fortran_mlcanopyfluxesmod/candidate"
sys.path.insert(0, str(cand))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, cand / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


module = load("mlcanopyfluxesmod_jax")
fn = module.mlcanopyfluxes_flat
signatures = module._SIGNATURES
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
        BitexactVerifier._type_recorded(np, [sample], signatures)
        return sample
    ins, recorded = parse_dump((dumps / f"mlcanopyfluxes_flat_{k:04d}.txt").read_text())
    sample = {"subprogram": "mlcanopyfluxes_flat", "inputs": ins, "outputs": recorded}
    BitexactVerifier._type_recorded(np, [sample], signatures)
    return sample


first = load_step(1)
carried_names = {n for n in (a["name"].lower() for a in sig["args"] if a["intent"] != "OUT") if n in first["outputs"]}
ncan = int(np.asarray(load_step(2)["inputs"]["mlcanopy_inst__ncan_canopy"])[0])

WATCH = ["tleaf_leaf", "tair_profile", "gppveg_canopy", "shflx_canopy", "lhflx_canopy", "tg_soil"]
watch_full = {w: f"mlcanopy_inst__{w}" for w in WATCH}


def dominant(got: np.ndarray, want: np.ndarray):
    if got.ndim >= 2 and got.shape[1] == 100:
        return got[:, :ncan], want[:, :ncan]
    if got.ndim >= 2 and got.shape[1] == 101:
        return got[:, : ncan + 1], want[:, : ncan + 1]
    return got, want


state: dict[str, np.ndarray] = {}
rows = []
print(f"steps={args.steps}  carried={len(carried_names)}  ncan={ncan}", flush=True)
for k in range(1, args.steps + 1):
    sample = first if k == 1 else load_step(k)
    kw = {}
    for name in taken:
        low = name.lower()
        kw[name] = state[low] if (low in state and k > 1) else sample["inputs"][low]
    result = fn(**kw)
    result = result if isinstance(result, tuple) else (result,)
    row = [float(k)]
    by_name = {}
    for name, got in zip(outs, result):
        low = name.lower()
        got = np.asarray(got)
        if low in carried_names:
            state[low] = got
        by_name[low] = got
    for w in WATCH:
        low = watch_full[w]
        got = by_name[low].astype(np.float64)
        want = np.asarray(sample["outputs"][low]).astype(np.float64)
        gd, wd = dominant(got, want)
        scale = max(float(np.abs(wd).max()) if wd.size else 0.0, 1e-30)
        absd = float(np.abs(gd - wd).max()) if wd.size else 0.0
        row += [absd, absd / scale, float(wd.mean()) if wd.size else 0.0, float(gd.mean()) if gd.size else 0.0]
    rows.append(row)
    if k % 96 == 0:
        print(f"step {k} done", flush=True)

traj = np.array(rows)
np.save(args.out, traj)
cols = ["step"] + [f"{w}_{s}" for w in WATCH for s in ("absd", "reld", "ref", "jax")]
print(f"columns: {cols}")
days = args.steps // 48
for i, w in enumerate(WATCH):
    ref = traj[:, 1 + 4 * i + 2].reshape(days, 48).mean(axis=1)
    jx = traj[:, 1 + 4 * i + 3].reshape(days, 48).mean(axis=1)
    rel = np.abs(jx - ref) / np.maximum(np.abs(ref), 1e-30)
    print(f"{w}: daily-mean rel max over {days} days = {rel.max():.3e}, median = {np.median(rel):.3e}")
print("DONE")
