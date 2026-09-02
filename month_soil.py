#!/usr/bin/env python3
"""31-day closed loop with the soil-temperature loop closed too.

    python month_soil.py [--steps 1488]

Per step, the driver's own sequence as three JAX kernels:
SoilThermProp -> MLCanopyFluxes -> SoilTemperature.  Carried closed-loop:
the canopy state (262 outputs), t_soisno, thk and bw; gsoi flows from the
canopy step into the soil advance.  Exogenous stays recorded: tower
forcing, the CLM per-step fields, and soil HYDROLOGY (h2osoi_liq --
SoilWater is outside the canopy+soil-thermal scope).  Verified against
the Fortran recording: carried t_soisno vs the recorded per-step input,
and the same daily-mean flux drift as month_jax.py.
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
parser.add_argument("--mode", choices=("numpy", "jax"), default="jax")
args = parser.parse_args()

CANO = HERE / "output/port/port-clm-ml/fortran_mlcanopyfluxesmod/candidate"
SOIL = HERE / "output/port/port-clm-ml/fortran_mlsoiltemperaturemod/candidate"
sys.path.insert(0, str(SOIL))
sys.path.insert(0, str(CANO))  # shared siblings byte-identical; whole-step first


def load(cand: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, cand / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


suffix = "_numpy" if args.mode == "numpy" else "_jax"
cano = load(CANO, f"mlcanopyfluxesmod{suffix}")
soil = load(SOIL, f"mlsoiltemperaturemod{suffix}")

CD = HERE / "output/recorded.31day/dumps/fortran_mlcanopyfluxesmod"
SD = HERE / "output/recorded.31day/dumps/fortran_mlsoiltemperaturemod"


def sig_of(mod, kern):
    sig = mod._SIGNATURES[kern]
    taken = [a["name"] for a in sig["args"] if a["intent"] != "OUT"]
    outs = [a["name"] for a in sig["args"] if a["intent"] in ("OUT", "INOUT")]
    return taken, outs


c_taken, c_outs = sig_of(cano, "mlcanopyfluxes_flat")
tp_taken, tp_outs = sig_of(soil, "soilthermprop_flat")
st_taken, st_outs = sig_of(soil, "soiltemperature_flat")


def load_cano(k: int) -> dict:
    with np.load(CD / f"mlcanopyfluxes_flat_{k:04d}.npz") as b:
        ins = {n[4:]: b[n] for n in b.files if n.startswith("in__")}
        rec = {n[5:]: b[n] for n in b.files if n.startswith("out__")}
    s = {"subprogram": "mlcanopyfluxes_flat", "inputs": ins, "outputs": rec}
    BitexactVerifier._type_recorded(np, [s], cano._SIGNATURES)
    return s


def load_soil(kern: str, k: int) -> dict:
    ins, rec = parse_dump((SD / f"{kern}_{k:04d}.txt").read_text())
    s = {"subprogram": kern, "inputs": ins, "outputs": rec}
    BitexactVerifier._type_recorded(np, [s], soil._SIGNATURES)
    return s


first = load_cano(1)
carried = {n for n in (a.lower() for a in c_taken) if n in first["outputs"]}
ncan = int(np.asarray(load_cano(2)["inputs"]["mlcanopy_inst__ncan_canopy"])[0])

T_SOISNO = "temperature_inst__t_soisno_col"
THK = "soilstate_inst__thk_col"
BW = "waterdiagnosticbulk_inst__bw_col"
GSOI = "mlcanopy_inst__gsoi_soil"

WATCH = ["tleaf_leaf", "tair_profile", "gppveg_canopy", "shflx_canopy", "lhflx_canopy", "tg_soil"]


def dominant(got, want):
    if got.ndim >= 2 and got.shape[1] == 100:
        return got[:, :ncan], want[:, :ncan]
    if got.ndim >= 2 and got.shape[1] == 101:
        return got[:, : ncan + 1], want[:, : ncan + 1]
    return got, want


state: dict[str, np.ndarray] = {}   # canopy carry (lowercase names)
soil_state: dict[str, np.ndarray] = {}  # t_soisno / thk / bw carry
rows, tso_err = [], []
print(f"mode={args.mode}  steps={args.steps}  canopy carried={len(carried)}  soil carried: t_soisno, thk, bw", flush=True)
for k in range(1, args.steps + 1):
    cs = first if k == 1 else load_cano(k)
    # SoilThermProp has two recorded call sites per step (the driver's, and
    # the one inside SoilTemperature, which the flat kernel inlines): the
    # driver-level call for step k is dump 2k-1.
    tp = load_soil("soilthermprop_flat", 2 * k - 1)
    st = load_soil("soiltemperature_flat", k)

    # 1) SoilThermProp: recorded step-k inputs, carries override
    kw = {n: tp["inputs"][n.lower()] for n in tp_taken}
    if k > 1:
        for key in (T_SOISNO, THK, BW):
            kw[key] = soil_state[key]
    r = soil.soilthermprop_flat(**kw)
    r = r if isinstance(r, tuple) else (r,)
    tpo = {n: np.asarray(v) for n, v in zip(tp_outs, r)}
    thk_k, bw_k = tpo[THK], tpo[BW]

    # 2) MLCanopyFluxes: canopy carry + soil-thermal carry
    kw = {}
    for n in c_taken:
        low = n.lower()
        kw[n] = state[low] if (low in state and k > 1) else cs["inputs"][low]
    if k > 1:
        kw[T_SOISNO] = soil_state[T_SOISNO]
    kw[THK] = thk_k
    res = cano.mlcanopyfluxes_flat(**kw)
    res = res if isinstance(res, tuple) else (res,)
    by = {}
    for n, got in zip(c_outs, res):
        low = n.lower()
        got = np.asarray(got)
        if low in carried:
            state[low] = got
        by[low] = got

    # 3) SoilTemperature: advance t_soisno with the canopy's gsoi
    kw = {n: st["inputs"][n.lower()] for n in st_taken}
    if k > 1:
        kw[T_SOISNO] = soil_state[T_SOISNO]
    kw[THK] = thk_k
    kw[BW] = bw_k
    kw[GSOI] = by[GSOI.lower()]
    r = soil.soiltemperature_flat(**kw)
    r = r if isinstance(r, tuple) else (r,)
    sto = {n: np.asarray(v) for n, v in zip(st_outs, r)}
    soil_state = {T_SOISNO: sto[T_SOISNO], THK: sto[THK], BW: sto[BW]}

    # verify carried t_soisno against the NEXT step's recorded input
    if k < args.steps:
        want = np.asarray(load_cano(k + 1)["inputs"][T_SOISNO.lower()], dtype=np.float64)
        got = np.asarray(sto[T_SOISNO], dtype=np.float64)
        m = np.abs(want) < 1e30  # dominant: skip spval padding
        scale = max(float(np.abs(want[m]).max()), 1e-30)
        tso_err.append(float(np.abs(got[m] - want[m]).max()) / scale)

    row = [float(k)]
    for w in WATCH:
        low = f"mlcanopy_inst__{w}"
        got = by[low].astype(np.float64)
        want = np.asarray(cs["outputs"][low]).astype(np.float64)
        gd, wd = dominant(got, want)
        scale = max(float(np.abs(wd).max()) if wd.size else 0.0, 1e-30)
        row += [float(np.abs(gd - wd).max()) / scale, float(wd.mean()), float(gd.mean())]
    rows.append(row)
    if k % 96 == 0:
        print(f"step {k} done  (t_soisno drift so far: max {max(tso_err):.3e})", flush=True)

traj = np.array(rows)
np.save(HERE / f"output/trajectory.soilclosed.{args.mode}.npy", traj)
days = args.steps // 48
print(f"\nt_soisno closed-loop drift vs recording: max {max(tso_err):.3e}  median {np.median(tso_err):.3e}")
for i, w in enumerate(WATCH):
    ref = traj[:, 1 + 3 * i + 1].reshape(days, 48).mean(axis=1)
    jx = traj[:, 1 + 3 * i + 2].reshape(days, 48).mean(axis=1)
    rel = np.abs(jx - ref) / np.maximum(np.abs(ref), 1e-30)
    print(f"{w}: daily-mean rel max = {rel.max():.3e}, median = {np.median(rel):.3e}")
print("DONE")
