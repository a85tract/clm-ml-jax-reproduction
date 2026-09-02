#!/usr/bin/env python3
"""Per-unit differential: the authors' clm-ml-jax functions on our recorded Fortran state.

    PYTHONPATH=../authors-clm-ml-jax/src python compare_authors_units.py [fortran:unit ...] [--calls 12,24,36,48]

For every recorded call of a unit (output/recorded/dumps/<unit>/<subprogram>_flat_KKKK.txt),
the recorded inputs are loaded into the authors' ``mlcanopy_type`` (1-based
padded arrays), their module singletons (``patch``, ``pftcon``, ``MLpftcon``,
the constant modules) are set to the recorded values, their function for that
subprogram is called, and every recorded output is compared entry by entry
with what they return -- the same oracle our own kernels were gated on.
Entries the Fortran left at spval are excluded, as in the engine's gate.
"""
from __future__ import annotations
import argparse
import importlib
import json
import sys
import traceback
from pathlib import Path

import numpy as np
np.seterr(all="ignore")
import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp
from recast.oracle.dump_replay import parse_dump

HERE = Path(__file__).resolve().parent
REC = HERE / "output/recorded/dumps"
CONST_MODULES = {
    "clm_varcon": "clm_src_main.clm_varcon", "clm_varpar": "clm_src_main.clm_varpar",
    "mlclm_varcon": "multilayer_canopy.MLclm_varcon", "mlclm_varctl": "multilayer_canopy.MLclm_varctl",
    "mlclm_varpar": "multilayer_canopy.MLclm_varpar", "clm_varctl": "clm_src_main.clm_varctl",
}

# subprogram -> (their module, their function, argument builder(header, filter, inst, extra))
def _bounds(x):
    from clm_src_main.decompMod import bounds_type
    return bounds_type(**{f: int(np.asarray(x.get(f"bounds__{f}", 1)).reshape(-1)[0]) for f in bounds_type._fields})

UNITS = {
    "leafheatcapacity":     ("MLLeafHeatCapacityMod", "LeafHeatCapacity", lambda h, f, i, x: (h["num_filter"], f, i)),
    "leafboundarylayer":    ("MLLeafBoundaryLayerMod", "LeafBoundaryLayer", lambda h, f, i, x: (h["num_filter"], f, h["il"], i)),
    "canopynitrogenprofile": ("MLCanopyNitrogenProfileMod", "CanopyNitrogenProfile", lambda h, f, i, x: (h["num_filter"], f, i)),
    "canopywettedfraction": ("MLCanopyWaterMod", "CanopyWettedFraction", lambda h, f, i, x: (h["num_filter"], f, i)),
    "canopyinterception":   ("MLCanopyWaterMod", "CanopyInterception", lambda h, f, i, x: (h["num_filter"], f, i)),
    "canopyevaporation":    ("MLCanopyWaterMod", "CanopyEvaporation", lambda h, f, i, x: (h["num_filter"], f, i)),
    "canopyturbulence":     ("MLCanopyTurbulenceMod", "CanopyTurbulence", lambda h, f, i, x: (h["nstep_ml"], h["num_filter"], f, i)),
    "leafphotosynthesis":   ("MLLeafPhotosynthesisMod", "LeafPhotosynthesis", lambda h, f, i, x: (h["num_filter"], f, h["il"], i)),
    "fluxprofilesolution":  ("MLFluxProfileSolutionMod", "FluxProfileSolution", lambda h, f, i, x: (h["num_filter"], jnp.array(f), i)),
    "longwaveradiation":    ("MLLongwaveRadiationMod", "LongwaveRadiation", lambda h, f, i, x: (_bounds(x), h["num_filter"], f, i)),
    "solarradiation":       ("MLSolarRadiationMod", "SolarRadiation", lambda h, f, i, x: (_bounds(x), h["num_filter"], f, i)),
    "soilfluxes":           ("MLSoilFluxesMod", "SoilFluxes", lambda h, f, i, x: (h["p"], i)),
    "leaffluxes":           ("MLLeafFluxesMod", "LeafFluxes", lambda h, f, i, x: (h["p"], h["ic"], h["il"], i)),
    "rungekuttaupdate":     ("MLRungeKuttaMod", "RungeKuttaUpdate", lambda h, f, i, x: (h["irk"], x["a"], x["b"], x["c"], h["num_filter"], jnp.array(f), i)),
    "plantresistance":      ("MLPlantHydraulicsMod", "PlantResistance", lambda h, f, i, x: (h["num_filter"], f, i)),
    "leafwaterpotential":   ("MLPlantHydraulicsMod", "LeafWaterPotential", lambda h, f, i, x: (h["num_filter"], f, h["il"], i)),
}


ZERO_BASED = {"rungekuttaupdate"}
SHOW = ""
LAYOUT = {"layout": "one"}


def actual(obj, field: str):
    """The object's field spelled the authors' way (they keep Fortran's case: iota_SPA, g0_BB)."""
    if hasattr(obj, field):
        return field
    names = getattr(obj, "_fields", None) or [n for n in dir(obj) if not n.startswith("_")]
    for n in names:
        if n.lower() == field.lower():
            return n
    return None


def fit(val, like: jnp.ndarray) -> jnp.ndarray:
    """A recorded (Fortran-shaped) array into the authors' padded shape: an axis
    one longer than ours is 1-based (index 0 unused), an equal one is 0-based."""
    a = np.asarray(val)
    if like.ndim == 0 or a.ndim == 0:
        return jnp.asarray(np.asarray(val).reshape(()), dtype=like.dtype) if like.ndim == 0 else fit(np.full(like.shape, a), like)
    if a.ndim != like.ndim:
        raise ValueError(f"rank {a.ndim} vs theirs {like.ndim}")
    out = np.array(like)
    out[slices(a.shape, like.shape)] = a
    return jnp.asarray(out, dtype=like.dtype)


def slices(ours, theirs):
    sl = []
    for s, t in zip(ours, theirs):
        if t == s + 1:
            sl.append(slice(1, t) if LAYOUT["layout"] == "one" or not sl else slice(0, s))
        elif t == s:
            sl.append(slice(0, t))
        else:
            raise ValueError(f"shape {ours} does not fit theirs {theirs}")
    return tuple(sl)


def run_unit(uid: str, calls: list[int]) -> dict:
    unit = uid.split(":")[1]
    ddir = REC / f"fortran_{unit}"
    subs = sorted({p.name.rsplit("_flat_", 1)[0] for p in ddir.glob("*_flat_*.txt")})
    result: dict = {}
    for sub in subs:
        if sub not in UNITS:
            result[sub] = {"status": "no adapter"}
            continue
        modname, fname, build = UNITS[sub]
        mod = importlib.import_module(f"multilayer_canopy.{modname}")
        fn = getattr(mod, fname)
        from multilayer_canopy.MLCanopyFluxesType import create_mlcanopy
        from clm_src_main import pftconMod, PatchType
        from multilayer_canopy import MLpftconMod
        per_output: dict[str, dict] = {}
        const_diffs: dict[str, tuple] = {}
        missing: set[str] = set()
        LAYOUT["layout"] = "zero" if sub in ZERO_BASED else "one"
        status = "ok"
        files = sorted(ddir.glob(f"{sub}_flat_*.txt"))
        chosen = [f for f in files if int(f.stem.rsplit("_", 1)[1]) in calls] or files[:1]
        for f in chosen:
            inputs, outputs = parse_dump(f.read_text())
            header = {k: int(v) for k, v in inputs.items() if "__" not in k and np.ndim(v) == 0 and k != "filter"}
            filt = tuple(int(v) for v in np.atleast_1d(inputs.get("filter", [1])))
            npatch = int(inputs.get("np_", 1))
            inst = create_mlcanopy(1, npatch)
            extra: dict = {}
            pftcon = pftconMod.pftcon
            mlpftcon = MLpftconMod.MLpftcon
            for name, val in inputs.items():
                if "__" not in name:
                    if name not in header and name != "filter":
                        extra[name] = val
                    continue
                owner, field = name.split("__", 1)
                if owner == "mlcanopy_inst":
                    fld = actual(inst, field)
                    if fld is None:
                        missing.add("" + field); continue
                    inst = inst._replace(**{fld: fit(val, getattr(inst, fld))})
                elif owner == "patch":
                    setattr(PatchType.patch, field, jnp.asarray(np.concatenate([[0], np.atleast_1d(val)]).astype(int)))
                elif owner == "pftcon":
                    fld = actual(pftcon, field)
                    if fld is None:
                        missing.add("pftcon." + field); continue
                    pftcon = pftcon._replace(**{fld: fit(val, getattr(pftcon, fld))})
                elif owner == "mlpftcon":
                    fld = actual(mlpftcon, field)
                    if fld is None:
                        missing.add("MLpftcon." + field); continue
                    mlpftcon = mlpftcon._replace(**{fld: fit(val, getattr(mlpftcon, fld))})
                elif owner in CONST_MODULES:
                    src = importlib.import_module(CONST_MODULES[owner])
                    have = getattr(src, field, None)
                    vv = np.asarray(val)
                    if have is not None and np.ndim(have) == 0 and vv.size == 1:
                        v = int(vv.reshape(())) if isinstance(have, (int, np.integer)) and not isinstance(have, bool) else float(vv.reshape(()))
                        if float(have) != float(v):
                            const_diffs[name] = (float(have), float(v))
                    else:
                        v = jnp.asarray(vv)
                    setattr(src, field, v)
                    if hasattr(mod, field):
                        setattr(mod, field, v)
                elif owner == "bounds":
                    extra[name] = val
                else:
                    extra[name] = val
            # rebind the singletons where the target module imported them by name
            for target in (mod, pftconMod):
                if hasattr(target, "pftcon"):
                    target.pftcon = pftcon
            for target in (mod, MLpftconMod):
                if hasattr(target, "MLpftcon"):
                    target.MLpftcon = mlpftcon
            if sub == "canopyturbulence" and hasattr(mod, "LookupPsihatINI"):
                mod.LookupPsihatINI()  # the RSL psihat tables their driver loads at init
            if "a" in extra:  # Runge-Kutta tableau: pad to their (1-based) shape
                ini = mod.RungeKuttaIni()
                extra["a"], extra["b"], extra["c"] = (fit(extra[k], jnp.asarray(t)) for k, t in zip("abc", ini))
            try:
                new = fn(*build(header, filt, inst, extra))
            except Exception as ex:  # noqa: BLE001
                status = f"raises {type(ex).__name__}: {str(ex).splitlines()[0][:120]}"
                break
            ncan = int(np.asarray(inputs.get("mlcanopy_inst__ncan_canopy", [100])).reshape(-1)[0])
            for name, rec in outputs.items():
                if not name.startswith("mlcanopy_inst__"):
                    continue
                field = name.split("__", 1)[1]
                fld = actual(new, field)
                if fld is None:
                    missing.add(field); continue
                theirs = np.asarray(getattr(new, fld))
                r = np.asarray(rec)
                t = theirs[slices(r.shape, theirs.shape)] if r.ndim else theirs
                mask = np.abs(r) < 1e30
                if r.ndim >= 2 and r.shape[1] in (100, 101):   # a layer axis: the canopy is layers 1..ncan
                    lay = np.zeros(r.shape, dtype=bool); lay[:, : ncan + (r.shape[1] - 100)] = True
                    outside = int(((t != r) & mask & ~lay).sum())
                    mask &= lay
                else:
                    outside = 0
                if SHOW and field == SHOW:
                    idx = np.argwhere((t != r) & mask)
                    print(f"    [{f.name}] {field}: {len(idx)} entries differ (of {int(mask.sum())}); first 12 (index, recorded, theirs):")
                    for ix in idx[:12]:
                        print(f"      {tuple(int(v) for v in ix)}  {r[tuple(ix)]:.12g}  {t[tuple(ix)]:.12g}")
                d = np.abs(t - r)[mask]
                rr = np.abs(r)[mask]
                st = per_output.setdefault(field, {"n": 0, "exact": 0, "max_abs": 0.0, "max_rel": 0.0, "max_ulp": 0.0, "outside_changed": 0})
                st["n"] += int(mask.sum()); st["exact"] += int((d == 0).sum()); st["outside_changed"] += outside
                if d.size:
                    st["max_abs"] = max(st["max_abs"], float(d.max()))
                    st["max_rel"] = max(st["max_rel"], float((d / np.maximum(rr, 1e-300)).max()))
                    st["max_ulp"] = max(st["max_ulp"], float((d / np.spacing(np.maximum(rr, 1e-300))).max()))
        result[sub] = {"status": status, "calls": [int(f.stem.rsplit('_', 1)[1]) for f in chosen], "outputs": per_output, "const_diffs": const_diffs, "missing": sorted(missing)}
    return result


parser = argparse.ArgumentParser()
parser.add_argument("units", nargs="*")
parser.add_argument("--calls", default="12,24,36,48")
parser.add_argument("--json", default=str(HERE / "output/compare_authors_units.json"))
parser.add_argument("--show", default="", help="print the differing entries of this output field")
args = parser.parse_args()
calls = [int(c) for c in args.calls.split(",")]
SHOW = args.show
units = args.units or [f"fortran:{d.name[8:]}" for d in sorted(REC.glob("fortran_*")) if d.name != "fortran_mlcanopyfluxesmod"]
ours = json.loads((HERE / "output/port/summary.json").read_text())
report: dict = {}
for uid in units:
    print(f"\n=== {uid}   (our JAX gate: {ours.get(uid, {}).get('verdict', '?')[:90]})")
    try:
        res = run_unit(uid, calls)
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        continue
    report[uid] = res
    for sub, r in res.items():
        if "outputs" not in r:
            print(f"  {sub}: {r['status']}"); continue
        print(f"  {sub}: {r['status']}  calls={r['calls']}")
        if r["missing"]:
            print(f"    fields the authors' types lack: {', '.join(r['missing'])}")
        for k, (theirs, rec) in r["const_diffs"].items():
            print(f"    constant {k}: theirs {theirs!r} recorded {rec!r}")
        for field, st in r["outputs"].items():
            extra = f"  outside-canopy entries changed={st['outside_changed']}" if st["outside_changed"] else ""
            print(f"    {field:22} n={st['n']:7d} exact={st['exact']:7d} max_abs={st['max_abs']:.3e} max_rel={st['max_rel']:.3e} max_ulp={st['max_ulp']:.3e}{extra}")
Path(args.json).write_text(json.dumps(report, indent=1))
