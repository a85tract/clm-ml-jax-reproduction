# Reproducing arXiv:2606.07681 under RecastEngine

**Paper.** Lahlou, Hawkins, Gentine (2026), *Systematic LLM Translation of Legacy
Scientific Code to Differentiable Frameworks: Application to a Land Surface
Model* — CLM-ml-v2 (Fortran) → `clm-ml-jax` via a five-phase agentic pipeline.

**Upstream source.** `gbonan/CLM-ml_v2.CHATS` @ `8d1cc40` (2025-12-04), cloned to
`upstream/` and never modified. The paper's `clm-ml-jax` code is not yet public
(nothing found on GitHub as of 2026-08-28), so the JAX side cannot be checked
against the authors' artifact.

**Status: 2026-08-28.** Everything below was run on macOS 26.5 / Apple silicon,
gfortran 16.1 (Homebrew), RecastEngine 0.0.1.dev0 with `recast-cesm` installed
(unused here — the run is engine-only, the way `corpus/` is held).

## Layout

| | |
|---|---|
| `upstream/` | the Fortran, read-only |
| `stage.py` | cpp-flattens the 76 `.F90` into `output/staged/` (`tools/corpus.py stage` for a case that lives outside the engine) |
| `run_translate.py [target]` | walks `translate` over every module unit, one unit per run so a crash is isolated; writes `output/baseline_<target>.json`, `output/translated/`, `output/evidence/` |
| `output/topo_order.txt` | the USE-dependency topological order (Phase 1 of the paper) |
| `build/` | the offline Fortran model, gfortran `-O2`, built in that order — `build.sh` |
| `build_O0/` | same, `-O0 -ffp-contract=off` |
| `build/run/`, `build_O0/run/` | May-2007 CHATS7 runs (`nl.CHATS7.05.2007`, output in `out/`) |

## What the paper maps to in the engine

| Paper phase | RecastEngine | Reached here |
|---|---|---|
| 1 Static dependency analysis, topological order | `FortranFrontend.discover` + USE graph | yes — 76 units, DAG, order in `output/topo_order.txt` |
| 2 State documents (CLAUDE.md / plan.md / CHANGELOG.md) | `Candidate.notes`, evidence manifests, `--summary` | n/a (engine records per run, not per session) |
| 3 Fortran oracle, per-module golden I/O | `f2py-golden` oracle | fails on every physics module — see below |
| 4 Translate → test → repair loop | `translate.numpy` (rules) or an agentic transform via `deferred_handler` | rules only: 0 / 76 units pass |
| 5 Full-column integration, gradients | no recipe; `port.jax` is numpy-anchored, per unit | full-column **Fortran** oracle built and run; no JAX |

## Reproduced

**Dependency graph (Appendix B.1).** 76 nodes (75 modules + 1 program) and
acyclic — both match the paper. Edge count depends on the convention: 279
module-header `USE` edges, 480 when subprogram-level `USE` is included
(deduplicated), 617 raw statements; the paper reports 315 and does not say how
it counted. Density 0.084 vs the paper's 0.055 follows from that.

**The Fortran reference runs.** The offline model builds with gfortran
(`-fno-range-check` needed: `CanopyStateType.F90:61` assigns `nan` to an integer
array) and completes May 2007 at CHATS7 — 1488 half-hourly steps in 7.3 s at
`-O2` (≈4.9 ms/step; the paper's 54 ms/sample on Derecho is a different
quantity and machine, not compared).

## Finding 1 — the Fortran oracle is compiler-dependent through undefined behaviour

The shipped `output_files/` (nvfortran) and my gfortran run disagree from the
first timestep, with relative RMSE up to 18 % in H and LE; `-O0` and `-O2`
gfortran builds disagree with each other from step 281 (8 steps differ by
> 1 W m⁻²). That is far beyond rounding.

Root cause (`upstream/multilayer_canopy/MLCanopyFluxesMod.F90`):

```
130:    real(r8) :: ark(nrk,nrk), brk(nrk), crk(nrk)        ! Runge-Kutta parameters
321:       call RungeKuttaIni (ark, brk, crk)          ! inside the first-call-only block
563:             call RungeKuttaUpdate (irk, ark, brk, crk, ...)   ! every timestep
```

The Butcher tableau lives in un-`SAVE`d locals, is filled once, and is read on
every later call. Standard Fortran leaves those values undefined after return;
it works only when the compiler happens not to reuse the stack slot. Evidence:

| build | vs shipped nvfortran `flux.out` |
|---|---|
| gfortran `-O0`, as shipped | max diff 63 W m⁻², 21 % of values bit-identical |
| gfortran `-O0 -finit-real=snan` | 20 818 / 26 784 values NaN from step 2 on |
| gfortran `-O0`, `save` added on line 130 (scratch copy only) | max diff 1.8 W m⁻², 99.4 % bit-identical; `-O0` vs `-O2` likewise 99.4 % |

So the shipped outputs were produced with the tableau intact, and every other
build is a roll of the dice. The paper's Phase-5 oracle was gfortran 12; its
"NSE 1.000" parity is a comparison against whichever tableau that build left
on the stack — reproducible only with the same binary.

The fix is one `save` (or making the arrays module-level). Per the relay rule
it is **not** applied in `upstream/` or anywhere in SciRecast; the scratch copy
that demonstrated it was discarded. The right action is an issue on
`gbonan/CLM-ml_v2.CHATS` — not filed yet, that is the user's call.

A second, smaller defect: `-finit-integer` / `-finit-logical` change nothing,
so the integer/logical state is clean.

## Finding 2 — the rule-driven `translate` recipe reaches no unit

`python run_translate.py numpy`, 76 units (`output/baseline_numpy.json`):

| stopped by | units | why |
|---|---|---|
| `static.rwset` | 48 | read/write sets disagree on nearly every block that touches a derived-type component through `associate` / pointer components (`mlcanopy_inst%…`) — the whole physics is written that way |
| `f2py-golden` | 26 | 12 constants-only modules with nothing to wrap (expected); the rest either take `TYPE(MLCANOPY_TYPE)` arguments the wrapper cannot spell (e.g. `MLMathToolsMod/hybrid`) or `include 'netcdf.inc'` with no include path handed to f2py |
| `differential.bitexact` | 1 | `histfilemod`: candidate imports `decompmod_numpy`, which was never emitted because that unit stopped earlier |
| engine crash | 1 | `surfacealbedomod`, below |
| passed | **0** | |

Refusals (blocks the rules would not guess), normalised: `call to external
subroutine` 49, `dim expr` 8, formatted internal write 7, `goto` 3, `inquire`
3, non-literal DATA bound 1, generic no-match 1. The paper's tiering agrees with
this picture: its Tier-1 (pure scalar) subroutines are the ones the rules could
in principle carry; Tier-2/3 are inside the derived-type loops that stop 48
units at the static gate.

This matches the engine's own corpus baseline (2 / 59 third-party units pass),
so it is not a CLM-ml surprise. The paper's result was obtained with an
LLM-in-the-loop transform plus hand-built per-module harnesses; the engine
ships the hook for that (`deferred_handler`, `AgentProvider`) and, in
`recast-cesm`, one such transform bound to CAM's stub tables. Reaching the
paper's Phase 4 in this framework means writing the CLM analogue of
`recast-cesm`: a frontend that knows `shr_kind_mod`/`clm_varcon`, a stub table
for `endrun`/`iulog`/netCDF/history, an agentic `translate.clm`, and — the
hard part — an oracle that can drive subprograms taking `mlcanopy_type`.

## Update 2026-08-28 (later) — `recast-clm`, and `MLWaterVaporMod` end to end

The gap named above is now a package: `../recast-clm/` (branch
`translate-clm`), the CLM analogue of `recast-cesm`, attached through entry
points only. What it took to carry the paper's simplest Tier-1 module through
all eight stages, bit-exact against the Fortran:

| plugin | what it answers |
|---|---|
| `clm` frontend | `r8` is 64-bit; `abortutils`, `clm_varctl`, `shr_kind_mod`, `clm_varcon`, `MLclm_varcon`, … are stubs, not companions |
| `translate.clm` | the framework stub tables (`endrun` raises, history/restart/netCDF are `pass`); **use-constants** — every name use-imported from a constants module is resolved from the tree (`recast.fortran.use.resolve`) into the candidate's own `<module>_use_constants.py`; **stand-ins** — the `abortutils_numpy.py`-style files the emitted header imports are written into the candidate, with the module's constants (same parsed expressions) and the framework calls a standalone run answers itself |
| `f2py-golden-clm` | the engine's oracle with the stub modules compiled in, `-I` for `netcdf.inc`, and `-lnetcdff` via `LDFLAGS` (the stub `abortutils` needs `nf_strerror` at load time); link flags folded into the cache key |
| `translate-clm` | the recipe, with land-surface sampling ranges on the gate |

```console
$ recast run translate-clm ../clm-ml-jax/output/staged --config ../clm-ml-jax/output/staged/recast.json --unit fortran:mlwatervapormod
fortran:mlwatervapormod
  [ok ] frontend   clm
  [ok ] transform  translate.clm
  [ok ] verifier   static.rwset                sampled: 8 blocks match
  [ok ] oracle     f2py-golden-clm             f2py:mlwatervapormod:444f824826717b73
  [ok ] verifier   differential.bitexact       bit_exact: 30 points across 2 subprogram(s), all bit-exact
  [ok ] verifier   symbolic.notary             symbolic: no rewrites to notarize; the translation is print-order faithful
  [ok ] store      fs-evidence                 3 verdict(s) recorded
```

`SatVap` 20 points and `LatVap` 10 points, `t` sampled in 200–330 K, max ULP
0. The paper's module bar was a relative tolerance of 1e-4; this is 0.

Engine defect 1 (the `lambda` result initializer) is fixed on a RecastEngine
branch, `clm-keyword-result` (`subprograms.py:_result_initializer` now spells
the result through `pysafe`; test added; suite green; the two `mypy` errors in
`interface.py` pre-exist on `main`). Defect 3 (`netcdf.inc`) is answered in
the extension's oracle rather than the engine, since it is CLM's stub that
needs it. Defects 2 and 4 stand.

Three things learned about the engine's contract on the way, worth relaying:

- the emitter binds every `use` of a non-companion module to an
  `import <module>_numpy` — so a domain package that declares stub modules
  must also supply those files, or the gate fails on the import;
- the gate takes the *last* `*_numpy.py` in `Candidate.files` as the module
  under judgement, so stand-ins have to be inserted before the unit's own;
- the f2py job's argv has no slot for linker flags; `LDFLAGS` in the
  environment is the only way in.

Full-tree walk with `translate-clm` (`python run_translate.py numpy
translate-clm` → `output/baseline_translate-clm_numpy.json`), 76 units:

| stopped by | `translate` (engine alone) | `translate-clm` |
|---|---|---|
| `static.rwset` | 48 | 49 |
| oracle | 26 | 23 — derived-type arguments (`TYPE(CLUMPFILTER)`, `TYPE(BOUNDS_TYPE)`, `TYPE(MLCANOPY_TYPE)`) and constants-only modules |
| `differential.bitexact` | 1 | 2 (`histfilemod`: nothing comparable; `initsubgridmod`: a stand-in for `patchtype` lacks the derived type) |
| engine crash | 1 | 1 (same `allocate(..., stat=)`) |
| **passed** | **0** | **1** — `mlwatervapormod` |

One more unit than the engine alone, and the honest reading is that the
extension's use-constants and stand-ins remove the *import* failures; what
stops everything else is the derived-type surface — `mlcanopy_inst%…` in the
static check, `TYPE(…)` dummies in the oracle — which is the next thing
`recast-clm` has to answer, and the paper's Tier-2/3 boundary exactly.

## Engine defects surfaced (not fixed here — relay rule; report to the translator's source repo)

1. **Python keyword as identifier.** `MLWaterVaporMod/LatVap` has a local named
   `lambda`. The emitter renames uses to `lambda_` but emits the initializer as
   `lambda = 0.0` → `output/translated/mlwatervapormod_numpy.py:626` is a
   `SyntaxError`; the unit stops at `static.rwset` with "emitted file does not
   parse". This is the paper's simplest Tier-1 module.
2. **Crash instead of refusal.** `allocate (albsat(mxsoil_color,numrad),
   albdry(mxsoil_color,numrad), stat=ier)` (`SurfaceAlbedoMod.F90:62`) raises
   `TypeError: string indices must be integers` in
   `recast/transform/numpy/statements.py:742` (`_allocate`, comparing a previous
   shape record that is a string). Contrary to the contract, it aborts the whole
   `run_recipe` rather than deferring the block; `run_translate.py` isolates it.
3. **f2py include path.** Units with `include 'netcdf.inc'` fail the oracle build
   with `Fatal Error: Cannot open included file 'netcdf.inc'` — the oracle has no
   way to be told an `-I` (`nf-config --includedir`).
4. **Derived-type arguments** stop the oracle for every physics subprogram —
   the known ceiling, recorded so the number is on the page: 0 of the 24
   `multilayer_canopy` units can be gated as they stand.

## Not reproduced (and why)

- The JAX translation itself, the 31-day parity (Fig. 5), gradient checks
  (§4.2), Jacobian (Fig. 6), calibration (Fig. 8), throughput (Fig. 9): all
  require `clm-ml-jax`, which is not released, or an agentic translation of the
  24 canopy modules, which is the multi-session effort the paper describes and
  outside what the rule engine does today.
- Finding 1 also means those comparisons need a Fortran oracle with the tableau
  bug closed before a tolerance of 1e-4 (module) or 1 % (column) is meaningful.

## Commands

```bash
cd ~/agent/SciRecast/RecastEngine && source .venv/bin/activate
python ../clm-ml-jax/stage.py
python ../clm-ml-jax/run_translate.py numpy
cd ../clm-ml-jax/build && ./build.sh && cd run && ../prgm.exe < nl.CHATS7.05.2007
```
