#!/usr/bin/env python3
"""Fig-8-style calibration: recover a stomatal parameter by gradient.

    python calibration.py [--steps 48] [--iters 40] [--perturb 1.5]

Synthetic-truth recovery: the recording IS the truth (made with the
namelist's iota_spa). Start the whole-step kernel from iota * perturb and
descend on the day's flux mismatch (GPP + LH, recorded inputs per step,
open loop) using the exact forward-mode derivative (jax.jvp) -- one
scalar multiplier, so forward mode is the efficient direction. Converging
back to multiplier 1 within a few percent is the claim."""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--steps", type=int, default=48)
parser.add_argument("--start", type=int, default=1)
parser.add_argument("--iters", type=int, default=40)
parser.add_argument("--perturb", type=float, default=1.5)
parser.add_argument("--dumps", default=str(HERE / "output/recorded.31day/dumps/fortran_mlcanopyfluxesmod"))
args = parser.parse_args()

cand = HERE / "output/port/port-clm-ml/fortran_mlcanopyfluxesmod/candidate"
sys.path.insert(0, str(cand))

def load(name):
    spec = importlib.util.spec_from_file_location(name, cand / f"{name}.py")
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

host = load("mlcanopyfluxesmod_numpy")
ported = load("mlcanopyfluxesmod_jax")
import jax, jax.numpy as jnp  # noqa: E402
from recast.verify.bitexact import BitexactVerifier  # noqa: E402

sig = ported._SIGNATURES["mlcanopyfluxes_flat"]
taken = [a["name"] for a in sig["args"] if a["intent"] != "OUT"]
outs = [a["name"] for a in sig["args"] if a["intent"] in ("OUT", "INOUT")]
gi = outs.index("mlcanopy_inst__gppveg_canopy")
li = outs.index("mlcanopy_inst__lhflx_canopy")
D = Path(args.dumps)

def load_step(k):
    with np.load(D / f"mlcanopyfluxes_flat_{k:04d}.npz") as b:
        ins = {n[4:]: b[n] for n in b.files if n.startswith("in__")}
        rec = {n[5:]: b[n] for n in b.files if n.startswith("out__")}
    s = {"subprogram": "mlcanopyfluxes_flat", "inputs": ins, "outputs": rec}
    BitexactVerifier._type_recorded(np, [s], ported._SIGNATURES)
    return s

samples = [load_step(k) for k in range(args.start, args.start + args.steps)]
iota_true = np.asarray(samples[0]["inputs"]["mlpftcon__iota_spa"])
gpp_scale = max(float(np.abs(np.asarray(s["outputs"]["mlcanopy_inst__gppveg_canopy"])).max()) for s in samples)
lh_scale = max(float(np.abs(np.asarray(s["outputs"]["mlcanopy_inst__lhflx_canopy"])).max()) for s in samples)
print(f"truth iota_spa (pft in use) = {iota_true[6]:.4f}; day scales gpp {gpp_scale:.3e} lh {lh_scale:.3e}")

def step_terms(mult, s):
    """One step's (gpp, lh) under the scaled parameter -- jvp is taken per
    step so the compiled graph is ONE whole-step kernel, not 48 of them."""
    kw = {n: s["inputs"][n.lower()] for n in taken}
    kw["mlpftcon__iota_spa"] = jnp.asarray(iota_true) * mult
    res = ported.mlcanopyfluxes_flat(**kw)
    return jnp.stack([res[gi][0], res[li][0]])


def day_loss(mult):
    total = 0.0
    for s in samples:
        g, l = np.asarray(step_terms(jnp.asarray(mult), s))
        eg = (g - float(s["outputs"]["mlcanopy_inst__gppveg_canopy"][0])) / gpp_scale
        el = (l - float(s["outputs"]["mlcanopy_inst__lhflx_canopy"][0])) / lh_scale
        total += eg**2 + el**2
    return total / len(samples)


def day_loss_and_grad(mult, h=1e-2):
    """Central finite difference of the jitted forward kernel: at 44 ms a
    step this is seconds per iteration, where re-tracing a jvp per step
    was minutes. The AD gradient itself is checked once below."""
    lo, hi = day_loss(float(mult) - h), day_loss(float(mult) + h)
    return (lo + hi) / 2, (hi - lo) / (2 * h)

mult = jnp.asarray(args.perturb)
lr = 0.4
print(f"start multiplier {float(mult):.4f}", flush=True)
# One exact forward-mode derivative at the start, against the FD: the
# optimization uses the cheap difference, the AD link is verified here.
_, (dg_ad, dl_ad) = jax.jvp(lambda m: step_terms(m, samples[min(24, len(samples)-1)]), (mult,), (jnp.ones(()),))
gp, lp = np.asarray(step_terms(mult + 1e-2, samples[min(24, len(samples)-1)])); gm, lm = np.asarray(step_terms(mult - 1e-2, samples[min(24, len(samples)-1)]))
print(f"AD check (noon step): d gpp/d mult AD {float(dg_ad):+.5e} vs FD {(gp-gm)/2e-2:+.5e}; "
      f"d lh/d mult AD {float(dl_ad):+.5e} vs FD {(lp-lm)/2e-2:+.5e}", flush=True)
prev_m, prev_g = None, None
for it in range(args.iters):
    loss, dldm = day_loss_and_grad(mult)
    if prev_g is not None and abs(dldm - prev_g) > 1e-12:
        # Barzilai-Borwein secant step: for a near-quadratic 1-D loss this
        # is Newton and lands in a few iterations.
        step = (float(mult) - prev_m) / (dldm - prev_g) * dldm
    else:
        step = 0.05 * (1 if dldm > 0 else -1)
    prev_m, prev_g = float(mult), float(dldm)
    mult = mult - jnp.clip(jnp.asarray(step), -0.25, 0.25)
    print(f"iter {it:3d}: loss {float(loss):.3e}  dL/dmult {float(dldm):+.3e}  mult {float(mult):.4f}", flush=True)
    if abs(float(dldm)) < 1e-6:
        break
print(f"FINAL multiplier {float(mult):.4f} (truth 1.0)  |error| {abs(float(mult)-1.0)*100:.2f}%")
