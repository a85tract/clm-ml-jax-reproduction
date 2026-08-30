#!/usr/bin/env python3
"""Port every recorded unit to JAX and gate it on its recording.

    python run_port.py [unit ...]

For each ``output/recorded/<unit>.json`` (or the units named), runs the
``port-clm-ml`` recipe with the same recording the NumPy translation was held
bit-exact against, and writes ``output/port/summary.json``: per unit the
verdict, which subprograms became JAX kernels, and why the rest did not.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
PORT = OUT / "port"
PORT.mkdir(exist_ok=True)

wanted = sys.argv[1:]
configs = sorted(OUT.glob("recorded/fortran_*.json"))
if wanted:
    configs = [c for c in configs if c.stem in {w.replace(":", "_") for w in wanted}]
summary: dict[str, dict] = {}
for path in configs:
    uid = path.stem.replace("fortran_", "fortran:")
    config = json.loads(path.read_text())
    stages = config.setdefault("stages", {})
    if "translate.clm-ml" in stages:
        stages["port.clm-ml-jax"] = stages.pop("translate.clm-ml")
    config["output"] = str(PORT)
    (PORT / path.name).write_text(json.dumps(config, indent=2))
    run = subprocess.run(
        ["recast", "run", "port-clm-ml", str(OUT / "staged"), "--config", str(PORT / path.name), "--unit", uid],
        capture_output=True,
        text=True,
    )
    text = run.stdout + run.stderr
    verdict = next((ln.strip() for ln in text.splitlines() if "differential.tolerance" in ln), "")
    stopped = next((ln.strip() for ln in text.splitlines() if "[!!]" in ln or "stopped" in ln), "")
    notes: dict = {}
    candidate = PORT / "port-clm-ml" / path.stem / "candidate"
    jax_file = candidate / f"{path.stem.replace('fortran_', '')}_jax.py"
    kernels: list[str] = []
    if jax_file.is_file():
        for line in jax_file.read_text().splitlines():
            if line.startswith("_JAX_KERNELS = "):
                kernels = json.loads(line.split("=", 1)[1].strip().replace("'", '"'))
    summary[uid] = {"verdict": verdict, "stopped": stopped, "kernels": kernels}
    print(f"{uid}: {verdict or stopped or text[-300:]}\n    kernels={kernels}")
(PORT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
