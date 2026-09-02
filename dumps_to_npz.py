#!/usr/bin/env python3
"""One-time: parse the whole-step text dumps into .npz beside them.

    python dumps_to_npz.py [--dumps DIR] [--workers 4]

Each ``mlcanopyfluxes_flat_KKKK.txt`` becomes ``mlcanopyfluxes_flat_KKKK.npz``
holding ``in__<name>`` and ``out__<name>`` arrays; ``column.py`` prefers the
.npz when it exists. Cuts a month's replay from ~1 s of text parsing per
step to milliseconds."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

parser = argparse.ArgumentParser()
parser.add_argument("--dumps", default=str(HERE / "output/recorded.31day/dumps/fortran_mlcanopyfluxesmod"))
parser.add_argument("--workers", type=int, default=4)
args = parser.parse_args()


def convert(path_str: str) -> str:
    from recast.oracle.dump_replay import parse_dump

    path = Path(path_str)
    target = path.with_suffix(".npz")
    if target.exists():
        return "skip"
    ins, outs = parse_dump(path.read_text())
    payload = {f"in__{k}": np.asarray(v) for k, v in ins.items()}
    payload.update({f"out__{k}": np.asarray(v) for k, v in outs.items()})
    np.savez_compressed(target, **payload)
    return "ok"


if __name__ == "__main__":  # macOS spawn re-imports __main__ in workers
    files = sorted(str(p) for p in Path(args.dumps).glob("mlcanopyfluxes_flat_*.txt"))
    print(f"{len(files)} dumps -> npz with {args.workers} workers", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        done = 0
        for r in pool.map(convert, files, chunksize=8):
            done += 1
            if done % 96 == 0:
                print(f"  {done}/{len(files)}", flush=True)
    print(f"converted {done}/{len(files)}")
