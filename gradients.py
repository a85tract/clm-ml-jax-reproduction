#!/usr/bin/env python3
"""Differentiate a ported kernel on the model's own state, and check it.

    python gradients.py fortran:mlleafheatcapacitymod [--sample 1]

For every ``<name>_flat`` kernel of the unit's ported module
(``output/port/port-clm-ml/<unit>/candidate/<module>_jax.py``) and every
real-valued input of the recorded sample: a forward-mode directional
derivative (``jax.jvp``) along a random direction, checked against a
central finite difference of the validated NumPy adapter on the same
recording; and, where reverse mode can trace the kernel, ``jax.grad`` of the
summed outputs, checked against the forward-mode derivative. What is
printed is the worst relative disagreement per input, and the reason where
reverse mode refuses -- a ``lax.fori_loop`` with a traced trip count lowers
to ``while_loop``, which has no reverse-mode rule.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

from recast.oracle.dump_replay import parse_dump
from recast.verify.bitexact import BitexactVerifier

HERE = Path(__file__).resolve().parent
PORT = HERE / "output" / "port"

parser = argparse.ArgumentParser()
parser.add_argument("unit")
parser.add_argument("--sample", type=int, default=1)
parser.add_argument("--step", type=float, default=1e-6)
args = parser.parse_args()

stem = args.unit.replace(":", "_")
module = args.unit.split(":", 1)[1]
candidate = PORT / "port-clm-ml" / stem / "candidate"
sys.path.insert(0, str(candidate))


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, candidate / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


host = load(f"{module}_numpy")
ported = load(f"{module}_jax")
import jax  # noqa: E402  (after the runtime enabled x64)
import jax.numpy as jnp  # noqa: E402

config = json.loads((PORT / f"{stem}.json").read_text())
dumps = Path(config["stages"]["dump-replay"]["dumps"])
kernels = ported._JAX_KERNELS
print(f"{args.unit}: kernels {kernels}")
rng = np.random.default_rng(0)

for kernel in kernels:
    files = sorted(dumps.glob(f"{kernel}_*.txt"))
    if not files:
        print(f"  {kernel}: no recording")
        continue
    inputs, outputs = parse_dump(files[min(args.sample, len(files)) - 1].read_text())
    sample = {"subprogram": kernel, "inputs": inputs, "outputs": outputs}
    BitexactVerifier._type_recorded(np, [sample], ported._SIGNATURES)
    sig = ported._SIGNATURES[kernel]
    taken = [a["name"] for a in sig["args"] if a["intent"] != "OUT"]
    base = {n: sample["inputs"][n.lower()] for n in taken}
    reals = [
        n
        for n in taken
        if isinstance(base[n], np.ndarray) and base[n].dtype == np.float64 and base[n].size
    ]

    def as_tuple(out):
        return out if isinstance(out, tuple) else (out,)

    # The finite difference runs the validated NumPy adapter where the unit
    # has one (its public subroutines); a private subprogram's flat kernel
    # has only itself to be differenced.
    reference = getattr(host, kernel, None) or getattr(ported, kernel)

    def numpy_side(**kw):
        copies = {k: (np.copy(v) if isinstance(v, np.ndarray) else v) for k, v in kw.items()}
        return [np.asarray(o, dtype=np.float64) for o in as_tuple(reference(**copies))]

    def jax_side(*reals_values):
        kw = dict(base)
        for name, value in zip(reals, reals_values, strict=True):
            kw[name] = value
        return [jnp.asarray(o, dtype=jnp.float64) for o in as_tuple(getattr(ported, kernel)(**kw))]

    print(f"  {kernel}: {len(reals)} real input(s), sample {files[0].parent.name}")
    x0 = [jnp.asarray(base[n]) for n in reals]
    for i, name in enumerate(reals):
        direction = rng.standard_normal(base[name].shape)
        tangents = [jnp.zeros_like(v) for v in x0]
        tangents[i] = jnp.asarray(direction)
        _, jvp_out = jax.jvp(jax_side, x0, tangents)
        h = args.step * max(1.0, float(np.abs(base[name]).max()))
        plus = dict(base)
        plus[name] = base[name] + h * direction
        minus = dict(base)
        minus[name] = base[name] - h * direction
        fd = [(a - b) / (2 * h) for a, b in zip(numpy_side(**plus), numpy_side(**minus), strict=True)]
        worst = 0.0
        for j, f in zip(jvp_out, fd, strict=True):
            j = np.asarray(j)
            scale = max(float(np.abs(f).max()), 1e-12)
            worst = max(worst, float(np.abs(j - f).max()) / scale)
        nonzero = any(float(np.abs(np.asarray(j)).max()) > 0 for j in jvp_out)
        print(f"    d/d{name}: jvp vs finite difference rel {worst:.2e}{'' if nonzero else ' (zero)'}")

    # Reverse mode on the summed outputs, against forward mode.
    def total(*reals_values):
        return sum(jnp.sum(o) for o in jax_side(*reals_values))

    try:
        grads = jax.grad(total, argnums=tuple(range(len(reals))))(*x0)
    except Exception as error:  # noqa: BLE001 -- the reason is the finding
        print(f"    reverse mode refused: {type(error).__name__}: {str(error).splitlines()[0][:120]}")
        continue
    for i, name in enumerate(reals):
        tangents = [jnp.zeros_like(v) for v in x0]
        tangents[i] = jnp.ones_like(x0[i])
        _, forward = jax.jvp(total, x0, tangents)
        against = float(jnp.sum(grads[i]))
        print(f"    grad wrt {name}: sum {against:.6e} vs jvp {float(forward):.6e}")
