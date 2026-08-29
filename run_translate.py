#!/usr/bin/env python3
"""Walk a translate recipe over every CLM-ml module; record per unit.

    python run_translate.py [target] [recipe]     # e.g. numpy translate-clm-ml

Mirrors tools/corpus.py run_case in the engine, on a case that lives outside it.
Writes output/baseline.json.
"""
from __future__ import annotations
import ast, collections, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
from recast.cli import _recipe
from recast.run import run_recipe
from recast.fortran.frontend import FortranFrontend

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
STAGED = OUT / "staged"
target = sys.argv[1] if len(sys.argv) > 1 else "numpy"
recipe_name = sys.argv[2] if len(sys.argv) > 2 else "translate"
found = FortranFrontend().discover(STAGED)
units = sorted(u.uid for u in found if u.kind in ("module", "program"))
print(f"{len(units)} units, target={target}, recipe={recipe_name}", flush=True)
t0 = time.time()
import traceback
class _R: pass
run = _R(); run.units = []; run.status = "mixed"; crashes = {}
recipe = _recipe(recipe_name)
for uid in units:
    t1 = time.time()
    try:
        r = run_recipe(recipe, STAGED, {"units": [uid], "output": str(OUT), "target": target})
        run.units.extend(r.units)
        print(f"  {uid:40} {[ur.stopped_by for ur in r.units]} {time.time()-t1:.0f}s", flush=True)
    except Exception as ex:
        crashes[uid] = "".join(traceback.format_exception_only(ex)).strip()[:300]
        print(f"  {uid:40} CRASH {crashes[uid][:120]}", flush=True)
print(f"run finished in {time.time()-t0:.0f}s", flush=True)

def norm(r):
    r = re.sub(r"^[\w/]+/B\d+:\s*", "", r); r = re.sub(r"'[^']*'", "'X'", r); r = re.sub(r"\b\d+\b", "N", r)
    return r[:90]

rec = {"units": {}, "crashes": crashes}
reasons = collections.Counter()
emitted = OUT / "translated"
if emitted.exists(): shutil.rmtree(emitted)
emitted.mkdir()
for ur in run.units:
    e = {"stopped_by": ur.stopped_by, "stages": {f"{o.kind}/{o.plugin}": o.status for o in ur.outcomes}}
    if ur.candidate is not None:
        e["deferred"] = len(ur.candidate.deferred)
        e["deferred_reasons"] = [norm(r) for r in ur.candidate.deferred]
        for r in ur.candidate.deferred: reasons[norm(r)] += 1
        for rel, text in ur.candidate.files.items():
            (emitted / Path(rel).name).write_bytes(text)
    for v in ur.verdicts:
        e.setdefault("verdicts", {})[v.verifier] = {"passed": v.passed,
            "metrics": {k: x for k, x in (v.metrics or {}).items() if not isinstance(x, list)},
            "detail": (v.detail or "")[:300]}
    rec["units"][ur.unit.uid] = e
rec["refusals"] = reasons.most_common()
(OUT / f"baseline_{recipe_name}_{target}.json").write_text(json.dumps(rec, indent=1, sort_keys=True))
stop = collections.Counter(e["stopped_by"] for e in rec["units"].values()); stop["CRASH"] = len(crashes)
print("stopped_by:", dict(stop))
print("top refusals:", reasons.most_common(15))
