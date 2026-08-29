#!/usr/bin/env python3
"""Stage CLM-ml_v2.CHATS for RecastEngine: cpp-flatten every .F90 into staged/."""
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
SRC = HERE / "upstream"
DIRS = ["clm_share", "clm_src_utils", "clm_src_main", "clm_src_biogeophys", "clm_src_cpl", "multilayer_canopy", "offline_driver"]
OUT = HERE / "output"
STAGED = OUT / "staged"
if STAGED.exists(): shutil.rmtree(STAGED)
STAGED.mkdir(parents=True)
n = 0
for d in DIRS:
    for f in sorted((SRC / d).glob("*.F90")):
        cmd = ["gfortran", "-E", "-P", "-cpp", f"-I{f.parent}", str(f)]
        text = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
        (STAGED / (f.stem + ".f90")).write_text(text); n += 1
(STAGED / "recast.json").write_text(json.dumps({"output": str(OUT)}, indent=2) + "\n")
print(f"staged {n} files -> {STAGED}")
