#!/usr/bin/env python3
"""Column-level comparison of the authors' clm-ml-jax against the Fortran reference.

    python compare_authors.py [--authors DIR] [--ref DIR]

Reads the six-file ascii output every driver writes (Fortran, the authors'
JAX driver, both in the same format) and reports, per flux.out column, the
Fig-5 metric month_jax.py uses for our own kernel: daily means over the 48
half-hour steps, relative difference per day, max and median over the days.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
COLS = ["time", "rnet", "stflx_air", "shflx", "lhflx", "gppveg", "ustar", "swup", "lwup",
        "tair_top", "gsoi", "rnsoi", "shsoi", "lhsoi", "lhflx_tr", "lhflx_ev", "beta", "stflx_veg"]

parser = argparse.ArgumentParser()
parser.add_argument("--ref", default=str(HERE / "output/recorded.31day/run/out"),
                    help="Fortran reference run (gfortran, tableau deviation staged)")
parser.add_argument("--authors", default=str(HERE.parent / "authors-clm-ml-jax/src/output_files/JAX_outputs_05_2007_31days"))
parser.add_argument("--also", nargs="*", default=[
    str(HERE / "upstream/output_files"),
    str(HERE / "build/run/out"),
    str(HERE / "build_O0/run/out"),
], help="other runs to report against the same reference")
parser.add_argument("--fields", nargs="*", default=["rnet", "shflx", "lhflx", "gppveg", "ustar", "lwup", "tair_top", "gsoi", "shsoi", "lhsoi"])
args = parser.parse_args()

def load(d: str) -> np.ndarray:
    a = np.loadtxt(Path(d) / "CHATS7_2007-05_flux.out")
    assert a.shape[1] == len(COLS), (d, a.shape)
    return a

ref = load(args.ref)
steps = ref.shape[0]
days = steps // 48
print(f"reference: {args.ref}  ({steps} steps, {days} days)")

def daily(v: np.ndarray) -> np.ndarray:
    nd = v.shape[0] // 48
    return v[: nd * 48].reshape(nd, 48).mean(axis=1)

def line(f: str, r: np.ndarray, c: np.ndarray) -> str:
    rd, cd = daily(r), daily(c)
    rel = np.abs(cd - rd) / np.maximum(np.abs(rd), 1e-30)
    scale = np.sqrt(np.mean(r * r)) or 1.0
    rms = np.sqrt(np.mean((c - r) ** 2)) / scale
    return f"  {f:10} {rel.max():19.3e} {np.median(rel):10.3e} {np.abs(cd - rd).max():16.3f} {rms:13.3e} {np.abs(c - r).max():16.3f}"

HEADER = f"  {'field':10} {'daily-mean rel max':>19} {'median':>10} {'max |daily diff|':>16} {'step rel-RMS':>13} {'max |step diff|':>16}"

def report(name: str, d: str) -> None:
    x = load(d)
    n = min(x.shape[0], steps)
    print(f"\n{name}: {d}  ({x.shape[0]} steps)")
    print(HEADER)
    for f in args.fields:
        i = COLS.index(f)
        print(line(f, ref[:n, i], x[:n, i]))

def report_ours(path: Path) -> None:
    """Our whole-step JAX kernel's closed-loop month (month_jax.py trajectory):
    columns step, then per watched field absd, reld, ref, jax."""
    if not path.is_file():
        return
    t = np.load(path)
    watch = ["tleaf_leaf", "tair_profile", "gppveg_canopy", "shflx_canopy", "lhflx_canopy", "tg_soil"]
    print(f"\nour JAX kernel (closed loop, recording as reference): {path}  ({t.shape[0]} steps)")
    print(HEADER)
    for w, f in [("gppveg_canopy", "gppveg"), ("shflx_canopy", "shflx"), ("lhflx_canopy", "lhflx")]:
        i = watch.index(w)
        print(line(f, t[:, 1 + 4 * i + 2], t[:, 1 + 4 * i + 3]))

report("authors' JAX", args.authors)
report_ours(HERE / "output/trajectory.fixed.npy")
for d in args.also:
    if Path(d, "CHATS7_2007-05_flux.out").is_file():
        report(Path(d).parent.name + "/" + Path(d).name, d)
