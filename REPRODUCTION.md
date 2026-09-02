# Reproducing arXiv:2606.07681 under RecastEngine

**Paper.** Lahlou, Hawkins, Gentine (2026), *Systematic LLM Translation of Legacy
Scientific Code to Differentiable Frameworks: Application to a Land Surface
Model* — CLM-ml-v2 (Fortran) → `clm-ml-jax` via a five-phase agentic pipeline.

**Upstream source.** `gbonan/CLM-ml_v2.CHATS` @ `8d1cc40` (2025-12-04), cloned to
`upstream/` and never modified. The paper's `clm-ml-jax` code is not yet public
(nothing found on GitHub as of 2026-08-28), so the JAX side cannot be checked
against the authors' artifact.

**Status: 2026-08-28.** Everything below was run on macOS 26.5 / Apple silicon,
gfortran 16.1 (Homebrew), RecastEngine 0.0.1.dev0 with a sibling CAM extension installed
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
`gbonan/CLM-ml_v2.CHATS` — filed 2026-08-31 with the user's approval:
https://github.com/gbonan/CLM-ml_v2.CHATS/issues/1.

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
the CAM extension, one such transform bound to CAM's stub tables. Reaching the
paper's Phase 4 in this framework means writing the CLM analogue of
a CAM-side extension: a frontend that knows `shr_kind_mod`/`clm_varcon`, a stub table
for `endrun`/`iulog`/netCDF/history, an agentic `translate.clm-ml`, and — the
hard part — an oracle that can drive subprograms taking `mlcanopy_type`.

## Update 2026-08-28 (later) — `recast-clm-ml`, and `MLWaterVaporMod` end to end

The gap named above is now a package: `../recast-clm-ml/` (branch
`translate-clm-ml`), a model-domain extension of the engine, attached through entry
points only. What it took to carry the paper's simplest Tier-1 module through
all eight stages, bit-exact against the Fortran:

| plugin | what it answers |
|---|---|
| `clm` frontend | `r8` is 64-bit; `abortutils`, `clm_varctl`, `shr_kind_mod`, `clm_varcon`, `MLclm_varcon`, … are stubs, not companions |
| `translate.clm-ml` | the framework stub tables (`endrun` raises, history/restart/netCDF are `pass`); **use-constants** — every name use-imported from a constants module is resolved from the tree (`recast.fortran.use.resolve`) into the candidate's own `<module>_use_constants.py`; **stand-ins** — the `abortutils_numpy.py`-style files the emitted header imports are written into the candidate, with the module's constants (same parsed expressions) and the framework calls a standalone run answers itself |
| `f2py-golden-clm-ml` | the engine's oracle with the stub modules compiled in, `-I` for `netcdf.inc`, and `-lnetcdff` via `LDFLAGS` (the stub `abortutils` needs `nf_strerror` at load time); link flags folded into the cache key |
| `translate-clm-ml` | the recipe, with land-surface sampling ranges on the gate |

```console
$ recast run translate-clm-ml ../clm-ml-jax/output/staged --config ../clm-ml-jax/output/staged/recast.json --unit fortran:mlwatervapormod
fortran:mlwatervapormod
  [ok ] frontend   clm
  [ok ] transform  translate.clm-ml
  [ok ] verifier   static.rwset                sampled: 8 blocks match
  [ok ] oracle     f2py-golden-clm-ml             f2py:mlwatervapormod:444f824826717b73
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

Full-tree walk with `translate-clm-ml` (`python run_translate.py numpy
translate-clm-ml` → `output/baseline_translate-clm-ml_numpy.json`), 76 units:

| stopped by | `translate` (engine alone) | `translate-clm-ml` |
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
`recast-clm-ml` has to answer, and the paper's Tier-2/3 boundary exactly.

## Update 2026-08-28 (night) — derived types: `mlcanopy_type` through the gate

`recast-clm-ml` now flattens a derived-type interface on both sides
(`flatten.py`): from the components a subprogram touches -- through its
`associate` aliases and the calls it passes the object to -- and their
`allocate (this%…)` bounds, it generates a Fortran `<name>_flat` that builds
the object and calls the original, and a Python `<name>_flat` that does the
same to the translation; the oracle precompiles the unit's whole `use`
closure into a static library and hands f2py only the adapter module. On
generated inputs (`np_ = 8` patches, the model's 100 layers, 2 leaf classes),
bit-exact:

| unit | compared | points |
|---|---|---|
| `mlwatervapormod` | SatVap, LatVap | 30 |
| `mlmathtoolsmod` | 7 of 10 public (hybrid/zbrent/bisection take a procedure dummy: ungated) | 2 140 |
| `mlleafheatcapacitymod` | LeafHeatCapacity, via the adapter | 8 000 |
| `mlleafboundarylayermod` | LeafBoundaryLayer, via the adapter | 48 000 |
| `mlsoilfluxesmod` | SoilFluxes, via the adapter | 480 |
| `mlcanopywatermod` | 3 subprograms, via adapters | 32 240 |
| `mlgetatmforcingmod` | 1, via the adapter | 1 360 |

Three findings on the way, each of which the gate produced rather than a
reading of the code:

1. **A translation defect, caught bit-exact.** `pftcon%slatop` is allocated
   `(0:mxpft)`; the translation read `slatop[itype - 1]`, one plant
   functional type off. The engine did not know a component's allocated
   lower bound. Fixed on `clm-keyword-result`: the frontend records
   `allocated_dims` from `allocate (this%…)`, the emitter shifts a
   `root%component` subscript by it, and an `associate` alias inherits its
   selector's bounds. LeafHeatCapacity went from 102/8000 points differing
   to 0.
2. **Upstream declares the object `intent(out)` and reads through it.**
   `MLSoilFluxesMod.f90:36` and two routines in `MLinitVerticalMod.f90`
   declare `type(mlcanopy_type), intent(out) :: mlcanopy_inst`, then read
   components on the next lines. By the standard the dummy is undefined on
   entry; it works because the components are pointers every compiler leaves
   associated. The engine's translation follows the standard (a fresh object)
   and the routine had no `tref_forcing`. The `clm` frontend re-declares such
   a dummy `inout` and records the assumption in `Facts.provenance`. Filed
   2026-08-31 beside the RK-tableau one:
   https://github.com/gbonan/CLM-ml_v2.CHATS/issues/2.
3. **Routines that check their own energy balance cannot be gated on
   generated inputs.** `LeafFluxes` computes `shleaf`, `lhleaf` from inputs
   and aborts if `rnleaf - shleaf - lhleaf - stleaf > 1e-3`; with `rnleaf`
   generated, it always aborts, on both sides. `FluxProfileSolution` the same.
   These need recorded state -- what the paper's Phase 3 produced by hand
   for 32 subroutines -- and the engine's `dump-replay` oracle is the slot for
   it. Not done.

Also stopped, honestly: `SolarRadiation` refuses `dim expr 'bounds % begp'`
(a local array dimensioned by a derived-type component: engine rule
missing); `hybrid`/`zbrent`/`bisection` take a procedure dummy (no adapter);
`initSubgridMod`/`FluxProfileSolution` reach components the transitive
analysis does not (depth or object aliasing), reported as `_Record has no
attribute`.

Full-tree walk after this round (`python run_translate.py numpy translate-clm-ml`,
76 units): **7 pass**, 8 reach the bit-exact gate and fail there (the three
findings above, plus components reached beyond the transitive analysis), 24
stop at the oracle (nothing spellable: procedure dummies, `bounds_type`,
character dummies -- the two `str is not flat` crashes are now refusals),
34 at the static gate (`call to external subroutine` 36 refusals, `dim expr`
8), and the engine `allocate(..., stat=)` crash stands. Against the engine
alone: 0 pass, 48 at the static gate.

## Update 2026-08-28 (late) — Phase 3: recorded state, and the solver bit-exact

`recast-clm-ml/record.py` is the paper's Phase 3 made mechanical: from the same
`FlatPlan` the adapters come from, it generates a Fortran recorder module
(one probe per adapted subprogram), brackets every `call <Name>(...)` in a
**copy** of the staged tree with the probes, builds that copy with the
engine's reference flags (`-O1 -fno-fast-math -ffp-contract=off`), runs the
CHATS7 namelist for one day, and writes the first 40 calls of each probe in
the engine's dump format. `clm-ml-jax/record.py` drives it; the dumps land
under `output/recorded/dumps/<unit>/` and `translate-clm-ml` replays them with
`{"oracle": "dump-replay"}` (`output/recorded/<unit>.json`).

| unit | on the model's own state | points |
|---|---|---|
| `mlleaffluxesmod` | LeafFluxes | 48 000 |
| `mlsoilfluxesmod` | SoilFluxes | 240 |
| `mlfluxprofilesolutionmod` | FluxProfileSolution -- the implicit solver, calling LeafFluxes, SoilFluxes and the tridiagonal solves | 4 000 |

All bit-exact. Two things the recording taught:

- **The recording's build is part of the reference.** Recorded under `-O2`,
  LeafFluxes differed by up to 4 301 ULP (max_rel 6e-13): FMA contraction,
  not the translation. Recorded under the engine's reference flags, 0 ULP.
  The dump format carries no build identity, so `RECORDING.md` beside the
  dumps does.
- **A second translation defect, caught by the recorded run.**
  `case (0, -1)` was emitted as `== 0 or == 1` -- the emitter walked the
  leaves under the selector and the unary minus is a node above the literal
  -- so `FluxProfileSolution` took the well-mixed branch under the implicit
  solver's setting and aborted. Fixed on `clm-keyword-result`; the fix also
  makes `case (lo:hi)` refuse, which the engine's inherited test had recorded
  as slipping past.

With these, ten units are bit-exact: seven on generated inputs, three on
recorded state. The recorded path is the one that scales to the rest of the
physics -- anything that checks its own balances, or whose inputs are
correlated -- and the per-unit cost is one line in `record.py`'s argument
list.

## Update 2026-08-29 — the canopy physics on recorded state: all 15 modules bit-exact

With recording generalized -- callbacks followed, every callee followed for
the module state it reads, run-time module variables (``nlevsno``,
``pftcon_val``, ``aH12``, the psihat grids) recorded and set on both sides,
run-time extents, the caller-buffer convention for every intent(out) array
-- the ``translate-clm-ml`` replay over the 15 canopy physics modules
(`python record.py …`, one day of CHATS7 May 2007, 40 calls per probe):

| unit | points, all bit-exact |
|---|---|
| LeafPhotosynthesis (FvCB + stomatal optimization through `hybrid`) | 160 200 |
| RungeKuttaUpdate | 140 200 |
| FluxProfileSolution (implicit solver, calling LeafFluxes/SoilFluxes/tridiag) | 84 400 |
| SolarRadiation (Norman + two-stream) | 68 680 |
| LeafFluxes | 48 000 |
| CanopyNitrogenProfile | 48 040 |
| LeafBoundaryLayer | 24 000 |
| CanopyTurbulence (Harman–Finnigan RSL, Obukhov secant through a callback) | 16 480 |
| LongwaveRadiation | 16 200 |
| CanopyWater (3 subprograms) | 16 120 |
| PlantHydraulics (3 subprograms, incl. SoilResistance over the soil column) | 13 080 |
| SoilTemperature (2 subprograms, the soil-column heat solver) | 8 400 |
| LeafHeatCapacity | 4 000 |
| InitVertical (3 subprograms) | 1 412 |
| SoilFluxes | 240 |

Plus MLMathToolsMod (7 of 10, sampled; hybrid/zbrent/bisection now
translate but take a procedure dummy the flat wrapper cannot spell),
MLWaterVaporMod and MLGetAtmForcingMod (sampled). That is every physics
module of `multilayer_canopy/` -- the paper's 73 module tasks were over the
same tree -- held bit-exact against the Fortran on the model's own state,
against the paper's 1e-4 module tolerance.

Engine work this round, all on `clm-keyword-result`: calls through a
procedure dummy bound to the module's interface bodies; `obj%comp` in
declared bounds; a subscript reads its lower-bound names, through an
associate alias too; stub and companion-global aliases in the read/write
protocol; `_f_copy_out` as a write; per-axis component lower bounds, with
expression bounds over visible or use-imported names, and an assumed-shape
dummy's declared lower bound; an opt-in caller-buffer convention for every
intent(out) array with the harness and signature table following; integer
parameters dividing as Fortran does; `case (0, -1)` keeping its sign; a
local's declared initializer honoured.

Findings the gate produced this round, each a wrong number before it was a
diagnosis: the well-mixed branch taken under the implicit setting
(`case (0, -1)` → `== 1`); `tbi_profile(begp:endp, 0:nlevmlcan)` read one
layer off; `col%dz(begc:endc, -nlevsno+1:nlevgrnd)` read one snow layer off
(twice: the component's bound and the alias's); `tair(p,:)` clobbered
above the canopy by a whole-array return; `nrk = runge_kutta_type/10`
rendered 4.1; `minlwp_SPA = -2._r8` and `unit_lai = 1.0_r8` started from 0;
a recording made under `-O2` differing by FMA contraction.

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

The config JSONs under `output/` (`recast.json`, `recorded*/fortran_*.json`,
`port/*.json`) name `output` and `dumps` relative to this directory; the
engine resolves them against the working directory, so run `recast` from here
(the scripts do).

```bash
cd RecastEngine && source .venv/bin/activate   # checkouts side by side: RecastEngine/, recast-clm-ml/, cesm/clm-ml-jax/
python ../clm-ml-jax/stage.py
python ../clm-ml-jax/run_translate.py numpy
cd ../clm-ml-jax/build && ./build.sh && cd run && ../prgm.exe < nl.CHATS7.05.2007
```

## Update 2026-08-29 (later) — JAX, through the flat functions

The paper's differentiable half. The engine's JAX backend excludes any
subprogram that takes a derived-type dummy -- every physics routine here --
and is not widened (its bytes are held to the script it came from).
Instead `port.tree-jax` (`recast/transform/jax/tree.py`) derives a *flat
function* per `FlatPlan` from the validated NumPy anchor: aliases and
`obj%comp` spelled as the flat arguments, module state the same, calls into
planned subprograms and into ported companions rewritten to their kernels,
the `return` replaced by the flat outputs; a dynamic slice masked over one
static length, a dynamic trip count made static with a guard (so reverse
mode has a rule), abort checks dropped and named. The untouched backend
lowers the result as an ordinary kernel. Recipe `port-clm-ml`: `clm-ml`
frontend, `port.clm-ml-jax`, `dump-replay` on the same recording the NumPy
translation was held bit-exact against, `differential.tolerance`
(`dominant_axis: all`, `rel_scale: array`).

`python run_port.py` (summary in `output/port/summary.json`):

| unit | JAX verdict | its physics as `lax` kernels |
|---|---|---|
| CanopyNitrogenProfile | toleranced, dominant within 0 ULP | yes |
| CanopyTurbulence | bit-exact 16,480 | AerodynamicConductance, ObuFunc, WindProfile, helpers; CanopyTurbulence/HF2008 delegated (`hybrid`) |
| CanopyWater | bit-exact 16,120 | all 3 |
| InitVertical | bit-exact 1,412 | 2 of 3 (`beta_distribution_cdf` not lowered) |
| LeafBoundaryLayer | within 1 ULP, 24,000 | yes |
| LeafFluxes | toleranced, dominant within 0 ULP, 40,220 | yes |
| LeafHeatCapacity | bit-exact 4,000 | yes |
| LeafPhotosynthesis | bit-exact 160,200 | CiFunc, StomataEfficiency, helpers; LeafPhotosynthesis itself delegated (`hybrid`/`zbrent` root finders) |
| PlantHydraulics | within 2 ULP, 13,080 | all 3 |
| RungeKutta | toleranced, dominant within 2 ULP, 55,486 | yes |
| SoilTemperature | within 4 ULP, 8,400 | both |
| FluxProfileSolution | **FAIL** at the ULP tier, but the defect is found and fixed: `tair` was planned read-only because the plan's scope lacked the companions' procedures (`call tridiag_2eq(..., tair(p,:), ...)`), an engine defect the NumPy adapter's in-place arrays hid. With it fixed every output agrees to 1e-12..6e-10 absolute; with jit *disabled* the kernel is bit-exact with the recording, so the residual is XLA's fusion -- the ULP-tier class the backend documents -- amplified by the iterative solve past the gate's 32 ULP | all 5 lowered |
| SolarRadiation | toleranced, dominant within 18 ULP, 37,120 (after: a local sized by a dummy extent takes the array dummy's static shape) | all 3 |
| Longwave | **FAIL** at the ULP tier: 6,092 ULP under jit, bit-exact with jit disabled -- XLA fusion, as FluxProfileSolution | both |
| SoilFluxes | **FAIL**: 2,399 ULP on `shsoi` (`tg - tair` amplifying a 4-ULP input difference) -- conditioning the gate's dominance test does not excuse | yes |

Derivatives (`python gradients.py fortran:<unit>`): forward mode agrees with
central finite differences of the NumPy adapter to ~1e-11 relative on the
recorded state; reverse mode (`jax.grad`) now traces every kernel whose
loops the rewrite made static, and agrees with forward mode (LeafHeatCapacity
d/d`slatop`: -4.715e5 both ways). Engine defects found on the way and fixed:
interface bodies' dummies recorded as module state; a bundled companion
handed the caller's use-constants; the backend carrying a step -1 loop's
hoisted bounds.

**Where the JAX numbers stand (2026-08-29, end).** With jit *disabled* -- the
same lowered code, XLA op by op, no fusion -- every one of the 15 units'
flat kernels reproduces its recording to 0 ULP on the first three recorded
calls, except CanopyNitrogenProfile (101 ULP), SolarRadiation (68) and
SoilTemperature (2), whose residuals are XLA's transcendentals rather than
libm's. Under jit, 12 of 15 pass `differential.tolerance`; the three that
do not (FluxProfileSolution, Longwave, SoilFluxes) differ from their
recordings only by what fusion changes, amplified by an iterative solve or
a cancellation past the gate's 32-ULP dominant bar. That is the backend's
documented ceiling, not a translation defect; whether the gate should
carry an "eager tier" for a ported kernel, or a per-unit `ulp_gate`, is a
policy the recipe's owner sets, and this reproduction leaves it at the
engine's default.

**Root finders, and the last two main kernels (2026-08-29, later).** `hybrid`,
`zbrent` and `bisection` take the object *and a procedure*; the port now
specializes each per callback (`hybrid__cifunc_flat`, ...), turns their
`while True ... break` and `while cond` into `lax.while_loop`, and merges
early returns into one exit. With that, LeafPhotosynthesis -- the paper's
headline kernel -- is a `lax` kernel within 28 ULP of its 160,200 recorded
points, root finders included, and CanopyTurbulence's (HF2008, GetObu,
RoughnessLength) within 24 ULP. Every one of the 15 modules' main physics
now lowers; the gate stands at 12/15, the three others the XLA-fusion
class already described. Derivatives of the LeafPhotosynthesis kernel:
forward mode agrees with finite differences to ~1e-11 for the leaf-state
inputs; with respect to `apar` -- which reaches the outputs only through
the root finder -- forward mode and the finite difference disagree
outright, an open item (the implicit-function derivative of an iteration
stopped on a tolerance is the honest comparison, not a finite difference
across a step count that changes). Reverse mode through `lax.while_loop`
is refused by JAX, as expected.

**Implicit-function adjoints and reverse mode (2026-08-29, latest).** Each
specialized root finder is now split into ``<spec>_iterate_flat`` (the
loop, its inputs and outputs detached) and the specialization the caller
sees, which adds ``-(F - sg(F))/sg(dF/dx)`` on the callback's residual at
the converged root: the value is exactly the iteration's (the Fortran
stopped on a tolerance; a Newton step would move it), the tangent the
implicit one, and the components carry the iteration's values with the
tangent of one more callback evaluation at the root -- the paper's §3.5
IFT fix, applied by rule. Loop bounds are left as Python ints so
``lax.fori_loop`` lowers to a ``scan`` that reverse mode can transpose
(a ``jnp.int32`` bound, even a concrete one, makes a ``while_loop``, which
it cannot). With that, ``jax.grad`` of the LeafPhotosynthesis kernel runs
and agrees with forward mode for every input, ``apar`` included; LeafFluxes
likewise. SolarRadiation still refuses reverse mode: a step -1 loop with a
run-time start (``do ic = ntop, nbot, -1``) is not yet made static. Open:
forward mode and the finite difference of the NumPy adapter still disagree
by ~30% for d(agross)/d(apar) on the summed outputs, while on a lit layer
the root's own derivative agrees with the residual's implicit derivative
(both zero: Rubisco-limited); the disagreement is therefore not in the
root finder and remains to be located.

**Reverse mode, where it stands (2026-08-29, latest).** Helpers now take the
module state they read as parameters (no module attribute is read at trace
time, which was a tracer leak under differentiation), and loops with a
run-time start (``do ic = nbot(p), ntop(p)``), a descending run-time
range, or a bound over a dummy extent (``do i = 2, n`` beside ``a(n)``) run
their axis's static extent under a guard. ``jax.grad`` runs on the
LeafPhotosynthesis and LeafFluxes kernels and agrees with forward mode.
SolarRadiation and CanopyTurbulence still refuse it: the backend's own
hoisting of a descending loop whose extent the rewrite could not read
from the body (``_cnt_n`` trip counts), and RoughnessLength's fixed-point
``while`` -- an iteration without a callback residual to hang an
implicit-function adjoint on, which the paper's approach would run as a
fixed-count ``fori_loop`` under a mask. Both are the next rules.

**Reverse mode everywhere tried (2026-08-29, end of day).** Counted
``while`` loops run as fixed-count ``for``s under their condition, loops
whose bound is a scalar integer dummy run to the indexed axis's static
extent under a guard (the bound is a tracer once the kernel is inlined),
and a loop after an early return takes the return flag in its condition
rather than being wrapped. ``jax.grad`` now runs and agrees with forward
mode on LeafPhotosynthesis, LeafFluxes, SolarRadiation, CanopyTurbulence,
SoilTemperature and PlantHydraulics; the gate stands at 12/15 with the same
three XLA-fusion residuals. Still open: d(agross)/d(apar) on 19 of 92
layers (~30%), not in the root finder; the three residuals; the full
column.

## Update 2026-08-30 — the whole time step as one flat unit, bit-exact

Phase 5 needs the orchestrator, not just its physics: `MLCanopyFluxes`
itself computes forcing interpolation (GetAtmForcing between the tower's
half-hours), the lai/dpai profiles, `rhg`, net radiation, the 6 ML
sub-steps with 5 Runge-Kutta passes each, the flux integration and the
diagnostics. Rather than hand-wiring the 15 ported kernels in Python, the
same record→translate pipeline was pointed at `mlcanopyfluxesmod` whole:
its flat plan carries 19 objects, 331 components and 122 module-state
inputs, and one recorded call is one CLM step (445 inputs, 259 outputs).

**Staged deviation (Finding 1 closed).** `stage.py` now moves
`call RungeKuttaIni (ark, brk, crk)` out of the first-call block so the
un-SAVEd tableau is filled every step — the same values with defined
behaviour, marked `staged deviation (Finding 1)` in the staged source. The
recording and every gate below stand on this build; the 15 physics
modules' JAX gates reproduce exactly (12/15, the same three XLA-fusion
residuals to the ULP).

**Engine additions the orchestrator forced** (RecastEngine branch
`column-orchestrator`): a character parameter is a value
(`calkindflag = 'GREGORIAN'` reached `isleap` at run time); a
subprogram-level `10 continue … go to 10` is a loop region the way the
statement-level rule already said; and the flat plan's callee closure is
transitive — `GetObu` calls `hybrid` in a module the orchestrator never
`use`s, and `ObuFunc`, reached only as `hybrid`'s callback, reads
`aH12` — so `_procedure_index` and `_state_vars` follow `use`/call
closure across companions of companions.

**Result.** `mlcanopyfluxes_flat` is bit-exact against the recording on
all 48 steps of the day — 902,544 points, `symbolic.notary`:
print-order faithful. The full canopy step — five nested call levels,
root finders included — is one NumPy function matching gfortran
bit-for-bit.

## Update 2026-08-30 (night) — the closed-loop column, bit-exact for a day

The recording itself yields the driver's contract: of the whole-step
adapter's 456 inputs, 262 are the previous step's own outputs — value for
value, every step — and 194 are exogenous (tower forcing, the CLM-side
per-step fields, `t_soisno`). `column.py` runs `mlcanopyfluxes_flat`
closed-loop on that split: state from its own outputs, forcing from the
recording. In `--mode numpy` the whole day — 48 CLM steps, 288 ML
sub-steps, 1440 RK stage evaluations — reproduces the Fortran run
bit-for-bit at every output of every step. The whole-step JAX kernel
(`mlcanopyfluxes_flat` emitted as one `lax` kernel, all 15 physics
companions inlined) runs and is compared on all 48 recorded steps:
669,387 of 902,544 points bit-exact under jit, the residual in the
10^-12..10^-9 relative band (the XLA-fusion class compounding over the
30 solver passes of a step); `--mode jax` measures how that residual
grows over the day.

**The whole-step residual characterized.** With jit disabled (eager jnp,
inputs as jnp arrays) the same ~140 outputs differ in the same
10^-12..10^-9 relative band, worst ~2e-9 (`dtair`/`dtleaf`, the RK slope
storage after 30 solver passes): the residual is the JAX/XLA numerical
tier itself — XLA's transcendental implementations and fusion — not a
translation defect, the same class the three per-module XLA residuals
documented. The apparently enormous ULP distances sit on spval-scale
(1e36) placeholder entries at relative distances ≤ 3e-11. Against the
paper's own §4.2 standard (1e-4 per module), the whole-step kernel is
five orders of magnitude inside tolerance at every recorded step.

## Update 2026-08-30 (Fig. 5) — the 31-day column, closed loop

A 31-day recording of the whole-step adapter (1488 calls, one per CLM
step, 4.7 GB of dumps; the 1-day recording preserved beside it) drives
`column.py` for the paper's full May-2007 CHATS7 window. In `--mode
numpy` the closed loop -- 1488 steps, 8928 ML sub-steps, 44,640 RK stage
evaluations, state carried entirely from the model's own outputs --
reproduces the Fortran month **bit-for-bit at every output of every
step**. Two boundaries of that claim: the soil column is not closed --
`t_soisno`, a prognostic advanced by `SoilTemperature` outside the canopy
call, is taken from the recording each step, as are the file-read CLM
fields (closing the soil loop means adding the gated
`soilthermprop`/`soiltemperature` kernels to the driver); and the parity
is *given the recorded exogenous forcing and soil state*. Within those
boundaries the paper's Fig. 5 claim (31-day parity within 1% column flux
tolerance) is met with zero tolerance on the NumPy translation; the JAX
kernel's month-long drift is measured by the same driver in `--mode jax`.
Sampling note: the per-module gates replay the recording's first day (48
calls per probed site; `initvertical` has 3), and MathTools was sampled
7/10 -- the whole-step gate covers every call of the recorded window.

**Fig. 5, closed (2026-08-30 night).** The whole-step JAX kernel, driven
closed-loop for the full month (1488 steps, ~7 minutes wall once the
step counter stays traced), does not diverge from the Fortran
trajectory: leaf temperature's per-step relative deviation holds at a
median 4.5e-11 (p95 1.7e-9, worst single instant 3.3e-3) with no growth
from day 1 to day 31. Against the paper's own Fig.-5 standard -- daily-
mean column fluxes within 1% -- the month gives GPP 1.0e-4, SH 9.6e-4,
LH 1.8e-4, soil T 9.5e-8: one to five orders inside tolerance. The
apparently large instantaneous relative errors on GPP-family outputs are
dawn/dusk near-zero divisions; at the aggregate level they vanish. The
same boundaries as the NumPy claim apply (recorded exogenous forcing;
soil column not closed).

**Fig. 9 (same-machine throughput).** One CLM step of the whole-step
kernel: 43.7 ms jitted (25.5 s one-time compile), against 377 ms for the
NumPy anchor and ~4.9 ms for the Fortran reference (-O2) -- all on this
laptop's CPU, single point. The 9x gap to Fortran is XLA dispatch
overhead on a problem this small; the paper's throughput claim lives on
GPU batch execution (Derecho) and is neither confirmed nor contradicted
by a single-point CPU number, as already noted.

**Reverse mode through the whole step (Fig. 6 groundwork, 2026-08-30
late).** What §4.2's per-module gradients did not face, the whole-step
kernel did: with every input linearized at once, `fwet = (h2ocan /
h2ocanmx) ** fwet_exponent` differentiates to infinity on a dry canopy
layer (`0 ** 0.67`), and inf x 0 seeds NaN into 124 of the step's
outputs -- with a ZERO input tangent, and invisibly to per-module probes
(their constants are never linearized). The chain of refusals before it
-- the substep and RK trip counts (`traced_scalars` keeps the per-step
counter `itim` out of the static arguments, which also ends the
compile-per-step the month run suffered), the calendar `while` under
`stop_gradient`, the layer loops whose counters ride into companion
kernels (extent inherited through the callee's kept associates) -- each
became an engine rule. The safe-pow emission (`where(x>0, x, 1) ** c *
where(x>0, 1, 0)`, fractional and run-set exponents alike) is
bit-identical for x > 0 (the gate's dominant artifact is byte-identical
around the change), keeps 0 ** c = 0, and takes the subgradient 0. After
it: zero NaN tangents across all 462 outputs, and `jax.grad` through the
full CLM step -- 30 solver passes, three root-finder specializations --
returns finite values agreeing with forward mode.

**Fig. 6, met (2026-08-30 night).** Reverse mode through the whole step
against forward mode, noon of day 1: d(SH)/d(forc_t) agrees to 2.2e-11
relative, d(LH) to 2.0e-11, d(Tg) to 1.9e-13 -- machine-precision
agreement on real daytime sensitivities through 30 solver passes and
three root-finder specializations. One caveat carried forward: both
modes give ~1e-19 (an effective zero) for d(GPP)/d(forc_t) at noon,
which should not vanish; this is the same broken-tangent family as the
open d(agross)/d(apar) item (the implicit-function detachment around the
photosynthesis root finder severing a path both modes lose alike), and
is tracked there -- the grad==jvp consistency claim itself is unaffected.

**Fig. 8, attempted -- and the honest result (2026-08-31 0:15).** The
calibration loop itself works end to end: iota_spa perturbed 1.5x, the
whole-step kernel driven over day 1, the loss falling monotonically with
a finite-difference gradient of the jitted kernel (~4 s per iteration),
and a one-shot AD-vs-FD check wired in. But it recovers only 1.50 ->
1.39 in 40 iterations: the parameter sensitivity through the stomatal
path is orders too small, and the AD check at noon gives exactly zero
for d(gpp, lh)/d(iota) -- the same severed-tangent family as
d(GPP)/d(forc_t) = 0 and the older d(agross)/d(apar) 30% item. Three
symptoms, one suspect: the implicit-function specialization around the
photosynthesis root finder detaches more than the iteration (the
components' dependence on parameters and forcing dies at the root).
Fig. 8 is therefore blocked on that one defect, not on machinery: fix
the IFT tangent, and both the GPP Jacobian entries and the calibration
convergence should come back together.

**The sensitivity "defect", resolved as the model's own fixed point
(2026-08-31).** Every symptom in yesterday's severed-tangent family
dissolves under per-entry scrutiny. (1) The old d(agross)/d(apar)
mismatch and every FD-vs-jvp zero were probe artifacts: summing a leaf
array puts ~1e38 of spval padding into the objective and a real 0.02
change rounds away in float64 -- jvp, working in tangent space where the
padding's tangents are zero, was right all along; per entry, JAX and
NumPy responses agree exactly. (2) The near-zero whole-step
d(GPP)/d(forc_t) and d/d(iota) at noon are the MODEL's true derivatives:
the Fortran recording itself carries gs bit-identical and agross within
one ULP step over step at quasi-steady noon -- the substep iteration
re-equilibrates ci (+11.6 ppm under +0.5 K) so assimilation returns to
its optimum; per-module sensitivities are large only because they hold
that equilibration fixed. AD, finite differences, and the Fortran
recording agree at every point tested. Consequences: the Fig-6 caveat is
retired (grad == jvp everywhere, and where both are zero the model is
zero); Fig-8's slow recovery is small genuine day-scale sensitivity
under re-equilibration -- an optimizer-scaling matter, not a defect.

**Correction and completion of the sensitivity story (2026-08-31).** The
"fixed point" reading of the noon zeros was wrong in an instructive way;
the full account has three parts, each now demonstrated. (i) Steps
1..~300 are CHATS leaf-out: layer apar is tiny and the WUE optimum sits
at gsmin -- the recording itself holds gs bit-identical at 0.002 for six
straight days -- so every "noon" probe aimed at day 1 measured a genuine
clamped-at-the-bound regime, zero sensitivity being the model's truth
there. (ii) On day 15 (leafed canopy) everything is alive: forc_t +0.5 K
moves gs by 2.6e-3 and agross by 3.7e-3; iota moves both. (iii) At fine
steps the true function is a STAIRCASE: the root finder's tolerance
quantizes the response (FD at h=0.075 on iota returns exactly zero;
larger-h secants bracket the jvp at -4.6e-4), so the implicit-function
derivative is the honest derivative of the smooth limit -- the paper's
own Sec. 3.5 position, here observed directly. Together with the
spval-summation probe artifact, every sensitivity discrepancy of the
last two days is accounted for; AD agrees with NumPy per entry, with
Fortran's recording, and with finite differences wherever finite
differences mean anything.

**Day-15 kernel regression: the callee-extent misfire (2026-08-31).**
The Fig-8 landscape scan was the instrument that caught it: loss at the
true multiplier came out 4.1e-3 instead of ~0, and the optimizer's
"recovered" 1.216 was compensating a kernel bias, not finding one. A
day-15 open-loop check (48 steps, recorded inputs) showed gppveg p95 13%
/ max 15.45%. Bisection across engine checkpoints (PYTHONPATH-swapped
emission, 3-step gpp probe): clean at 2376be4 (8.8e-14), broken from
fe8c74f (1.55e-1) -- the callee-extent commits. The smoking gun in the
emission diff: the RK stage loop `do irk = 1, nrk_steps+1` (5 passes;
the final combination pass does not index dtg) had its bound rewritten
to `fori_loop(1, dtg_soil.shape[1] + 1)` = 4 passes -- the callee-extent
rule inherited the 4-stage dtg axis for a loop that legitimately runs
one pass PAST that axis, and a too-short range is a wrong answer no
guard can widen. Day 1 hid it (the canopy barely evolves); the day-1
gate was blind by construction. Fix (engine 13debff): the callee extent
is taken only when the stop expression subscripts a per-patch count
(`ncan[p-1] + 1`, the pattern the rule was built for); scalar bounds
stay as written and are trace-time static on their own. After the fix
the day-15 48-step open-loop errors are gppveg max 3.4e-5 (tolerance
staircase steps), lhflx/shflx/ustar <= 3e-10; the day-1 differential
metrics return byte-identical to the pre-regression fingerprint
(667863 bit-exact / max_rel 193.4 on the strict 32-ULP whole-step gate,
which the JAX kernel has never been expected to pass -- the staircase
amplifies ULP-level XLA reassociation; the paper-level criterion is the
Fig-5 1% band). Lesson, now standing policy: every kernel gate runs
day-15 (active canopy, live root finder) steps alongside day 1.

**Fig 8 closed (2026-08-31, fixed kernel).** Synthetic-truth recovery of
the stomatal efficiency iota on day 15 (48 recorded-input steps, open
loop, GPP+LH mismatch): loss at the true multiplier is 1.9e-6 (the
staircase floor; it was 4.1e-3 on the broken kernel), and secant descent
from a 1.5x perturbation recovers multiplier 0.9995 -- 0.05% from truth
-- in 7 iterations. Fig-6 rows re-verified on the fixed kernel at
day-15 noon (step 697): d(SH)/d(forc_t) grad == jvp to 2.8e-12,
d(LH)/d(forc_t) to 6.0e-11, d(Tg)/d(forc_t) to 9.9e-14.

**Fig 5 re-confirmed on the fixed kernel (2026-08-31).** Full 31-day
closed-loop JAX run (`month_jax.py`, 1488 steps, state carried from the
kernel's own outputs): daily-mean relative drift vs the Fortran
recording -- GPP 1.041e-4, SH 9.634e-4, LH 1.757e-4, Tleaf 2.97e-6,
Tair 1.36e-6, Tg 9.5e-8 -- all well inside the paper's 1% band, and the
flux numbers identical to the pre-regression run, confirming the fix
restored value semantics exactly. Trajectory in
`output/trajectory.fixed.npy`, log in `output/column_jax_month.fixed.log`.

**The soil-thermal loop, closed (2026-08-31).** `month_soil.py` runs the
driver's own per-step sequence as three kernels -- SoilThermProp ->
MLCanopyFluxes -> SoilTemperature -- carrying t_soisno, thk and bw
closed-loop alongside the canopy state, with gsoi flowing from the
canopy step into the soil advance; only hydrology (`h2osoi_liq`, from
SoilWater) and the tower forcing stay recorded. The soil unit was
re-recorded over the month (4,464 dumps; SoilThermProp has TWO call
sites per step -- the driver's and the one inside SoilTemperature that
the flat kernel inlines -- so the driver-level dump for step k is
2k-1; a first run mis-indexed this and showed a spurious 1.4e-3
t_soisno drift *identical in NumPy and JAX*, which is exactly the
signature that separates a wiring error from a numerical tier). With
the indexing right, the recorded hand-off soiltemp_out(k) ->
thermprop_in(k+1) is bit-equal at every probe, and: the **NumPy**
soil-closed month is **bit-for-bit zero** at every output of every one
of the 1,488 steps; the **JAX** month drifts t_soisno by at most
2.4e-6 (median 9e-11), with daily-mean fluxes GPP 1.009e-4,
SH 8.735e-4, LH 1.766e-4, Tg 1.1e-7 -- the same XLA tier as the
canopy-only loop, still one to four orders inside the paper's 1% band.
The remaining exogenous boundary is soil hydrology and the forcing.
Artifacts: output/trajectory.soilclosed.{numpy,jax}.npy,
output/column_jax_month.soilclosed.log,
output/recorded.31day/dumps/fortran_mlsoiltemperaturemod/.
