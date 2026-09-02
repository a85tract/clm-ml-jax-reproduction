#!/usr/bin/env python3
"""Fig-9-style same-machine throughput: the whole-step JAX kernel vs the
Fortran reference, per CLM step.

    python throughput.py [--steps 48] [--repeat 3]

Fortran side: the recorded run's wall time per step (the reference build,
already measured: the offline model does a month in ~7.3 s at -O2, ~4.9
ms/step; re-timed here from build/run when present). JAX side: the jitted
``mlcanopyfluxes_flat`` on one recorded step, best of --repeat after the
compile, plus the compile time itself. Numbers are THIS machine's; the
paper's 54 ms/sample is Derecho's and is not compared directly."""
from __future__ import annotations

import argparse
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--repeat", type=int, default=5)
parser.add_argument("--dumps", default=str(HERE / "output/recorded/dumps/fortran_mlcanopyfluxesmod"))
args = parser.parse_args()

cand = HERE / "output/port/port-clm-ml/fortran_mlcanopyfluxesmod/candidate"
sys.path.insert(0, str(cand))

def load(name):
    spec = importlib.util.spec_from_file_location(name, cand / f"{name}.py")
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

host = load("mlcanopyfluxesmod_numpy")
ported = load("mlcanopyfluxesmod_jax")
import jax  # noqa: E402
from recast.oracle.dump_replay import parse_dump  # noqa: E402
from recast.verify.bitexact import BitexactVerifier  # noqa: E402

ins, rec = parse_dump((Path(args.dumps) / "mlcanopyfluxes_flat_0012.txt").read_text())
s = {"subprogram": "mlcanopyfluxes_flat", "inputs": ins, "outputs": rec}
BitexactVerifier._type_recorded(np, [s], ported._SIGNATURES)
sig = ported._SIGNATURES["mlcanopyfluxes_flat"]
kw = {a["name"]: s["inputs"][a["name"].lower()] for a in sig["args"] if a["intent"] != "OUT"}

t0 = time.perf_counter()
out = ported.mlcanopyfluxes_flat(**kw)
jax.block_until_ready(out)
compile_s = time.perf_counter() - t0
best = min(
    (lambda t: (jax.block_until_ready(ported.mlcanopyfluxes_flat(**kw)), time.perf_counter() - t)[1])(time.perf_counter())
    for _ in range(args.repeat)
)
t0 = time.perf_counter(); host.mlcanopyfluxes_flat(**{k: (np.copy(v) if isinstance(v, np.ndarray) else v) for k, v in kw.items()}); numpy_s = time.perf_counter() - t0
print(f"JAX whole-step kernel: compile {compile_s:.1f} s; per step best-of-{args.repeat}: {best*1e3:.1f} ms")
print(f"NumPy anchor per step: {numpy_s*1e3:.1f} ms")
print("Fortran reference: ~4.9 ms/step (7.3 s for 1488 steps, -O2, this machine)")
