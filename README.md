# clm-ml-jax-reproduction

An independent reproduction of

> Lahlou, Hawkins, Gentine (2026). *Systematic LLM Translation of Legacy
> Scientific Code to Differentiable Frameworks: Application to a Land Surface
> Model.* [arXiv:2606.07681](https://arxiv.org/abs/2606.07681)

The paper translates CLM-ml-v2, Bonan's multilayer-canopy land model written
in Fortran, into JAX with a five-phase agentic pipeline, then shows that the
result runs a 31-day tower-site simulation in agreement with the Fortran
(Fig. 5), yields consistent Jacobians (Fig. 6), recovers a parameter by
gradient-based calibration (Fig. 8), and runs faster (Fig. 9).

This repository redoes that translation with a different instrument,
[RecastEngine](https://github.com/a85tract/RecastEngine): a rule-driven
Fortran-to-Python/JAX engine that verifies every generated unit against the
original Fortran, and records the evidence. Nothing here is the paper's code
and nothing here was written by hand to match it; the JAX is generated, and the
report says exactly where it agrees with the Fortran and where it does not.

## Where the code is

| What | Where |
|---|---|
| The paper's own translation | [`AyaLahlou/clm-ml-jax`](https://github.com/AyaLahlou/clm-ml-jax) (BSD-3). Compared against the same Fortran oracle, see below. |
| The Fortran being translated | [`gbonan/CLM-ml_v2.CHATS`](https://github.com/gbonan/CLM-ml_v2.CHATS) at `8d1cc40`. Clone it into `upstream/` (not committed here; never modified). |
| The engine | [`a85tract/RecastEngine`](https://github.com/a85tract/RecastEngine). Its condensed account of this case: [`docs/case-clm-ml.md`](https://github.com/a85tract/RecastEngine/blob/main/docs/case-clm-ml.md). |
| The CLM-ml domain extension for the engine | `recast-clm-ml` (private at the time of writing; the frontend, stub table and recipes for this model). |
| **The generated JAX and NumPy** | `output/port/port-clm-ml/<unit>/candidate/*_jax.py`, `*_numpy.py`. The whole time step as one JAX kernel is `mlcanopyfluxes_flat` in `fortran_mlcanopyfluxesmod/`. |
| The scripts that drive the reproduction | this directory, see below |

## Where the results are

**[`REPRODUCTION.md`](REPRODUCTION.md)** is the complete record, written as
the work happened (2026-08-28 to 2026-09-02): what was run, what agreed, what
failed and why, and the defects found in the upstream Fortran and in the
engine. Read that for the details. The headline numbers, all measured against
the Fortran run on the same laptop:

| Paper claim | Reproduced | Evidence |
|---|---|---|
| **Fig. 5** 31-day closed-loop column, fluxes within 1% | JAX daily-mean drift vs Fortran: GPP 1.0e-4, SH 9.6e-4, LH 1.8e-4, Tg 9.5e-8. The NumPy column is bit-for-bit zero at every output of all 1,488 steps. | `output/column_jax_month.fixed.log`, `output/trajectory.fixed.npy`, `month_jax.py` |
| **Fig. 6** Jacobian rows, reverse vs forward mode | `jax.grad` through the whole step equals `jax.jvp` to 2.8e-12 (SH), 6.0e-11 (LH), 9.9e-14 (Tg) at day-15 noon | `output/fig6_day15_noon.fixed.log`, `gradients.py` |
| **Fig. 8** parameter recovery by gradient calibration | stomatal efficiency recovered to 0.05% of truth from a 1.5x perturbation, 7 iterations | `output/calibration.fixed.log`, `calibration.py` |
| **Fig. 9** throughput | 43.7 ms per step jitted (25.5 s one-time compile), NumPy 377 ms, Fortran 4.9 ms, all CPU single-point; not comparable to the paper's GPU figure | `throughput.py` |
| Per-module translation | 15/15 canopy physics modules bit-exact in NumPy on recorded state; 12/15 pass the JAX 32-ULP gate under `jit`, the other three (FluxProfileSolution, Longwave, SoilFluxes) are exact with `jit` off and differ only by XLA fusion | `output/port/summary.json`, `output/run_port.regate2.log` |
| Beyond the paper | soil-thermal loop also closed (NumPy zero drift over the month; JAX 2.4e-6) | `output/column_jax_month.soilclosed.log`, `month_soil.py` |
| Against the authors' translation | same oracle, same month: their driver's SH step-RMS 5.5e-3 vs our kernel's 7.4e-4 (nvfortran-vs-gfortran is 7.9e-4); per unit, theirs is exact or ULP-tier wherever the Fortran is closed-form, and off by the Fortran's own solver tolerance where it iterates (gs 3%, Obukhov 0.2%); ours is 0 ULP there | `compare_authors.py`, `compare_authors_units.py`, `output/compare_authors_units.log` |

Two defects in the upstream Fortran surfaced on the way and were reported
there: the Runge-Kutta tableau kept in un-SAVEd locals
([CLM-ml_v2.CHATS#1](https://github.com/gbonan/CLM-ml_v2.CHATS/issues/1))
and `intent(out)` arguments read on entry
([#2](https://github.com/gbonan/CLM-ml_v2.CHATS/issues/2)). The first makes
the Fortran reference itself compiler-dependent; the staged sources carry a
marked one-line deviation that gives it defined behaviour.

## What the comparison with the authors' code shows

The authors' translation, [`AyaLahlou/clm-ml-jax`](https://github.com/AyaLahlou/clm-ml-jax),
was run against the same Fortran oracle as ours, both per module on recorded
state and as a whole month (details and numbers in
[`REPRODUCTION.md`](REPRODUCTION.md), section "differential against the
authors' own translation"). In plain terms:

**Where the two translations differ.** Wherever the Fortran is a closed
formula, both translations reproduce it exactly or to a few ULP. Wherever
the Fortran iterates a solver to a tolerance, the authors replaced the
loop with a fixed number of iterations (their code marks this as a
physical approximation, done for `jit` and differentiability), so their
values land within the Fortran's own tolerance of the recorded ones
(stomatal conductance up to 3%, Obukhov length 0.2%); ours reproduce the
Fortran's iteration path bit for bit. Over a month that is the whole
difference: sensible heat step-RMS 5.5e-3 for their shipped run against
7.4e-4 for ours, where two Fortran compilers differ by 7.9e-4. Both are
inside the paper's 1% band. This is a design trade-off, not an error.

**What we could not reproduce.** The 31-day output file the authors ship
in their repository agrees with the Fortran to the third decimal over its
first two days. Their code, run on this machine (CPU, jax 0.11.1, x64),
does not produce that file: neither the current `main` nor the commit
that added the file matches it (62 of the first 96 steps differ), and
both show the same isolated excursions of up to 27 W/m2 at a handful of
steps that the shipped file does not have. We do not know on what
machine, JAX version, or code state the shipped file was made, and we have
not traced the excursions to a cause. These are open questions for the
authors, not findings against the code.

## Layout

| | |
|---|---|
| `stage.py` | cpp-flattens the upstream `.F90` into `output/staged/` |
| `record.py` | builds a Fortran recorder, runs May 2007 at CHATS7, dumps every probed call's inputs and outputs |
| `run_translate.py`, `run_port.py` | translate to NumPy, port to JAX, gate each unit against its recording |
| `column.py`, `month_jax.py`, `month_soil.py` | the closed-loop column: one day, 31 days, 31 days with the soil-thermal loop |
| `gradients.py`, `calibration.py`, `throughput.py` | Fig. 6, Fig. 8, Fig. 9 |
| `output/recorded/` | 1-day recording of all 16 units (48 calls each) |
| `output/recorded.soil-month/`, `output/recorded.bak-20260830/` | the soil-loop month recording; the pre-tableau-fix per-unit recording |
| `output/port/`, `output/translate*/` | generated candidates and the engine's evidence for every run |
| `output/*/staged/` | not committed (upstream source); `stage.py` regenerates it |
| 31-day whole-step recording (5.3 GB) | not in git: the [`recording-31day-20260830`](https://github.com/a85tract/clm-ml-jax-reproduction/releases/tag/recording-31day-20260830) release, unpack into `output/` |

Config JSONs under `output/` name paths relative to this directory; run
`recast` from here.

## Running it

Needs gfortran and netCDF-Fortran, RecastEngine and `recast-clm-ml` installed
in one environment, and the upstream clone in `upstream/`.

```bash
python stage.py
python record.py fortran:mlleaffluxesmod ... fortran:mlcanopyfluxesmod --days 1 --calls 48
python run_port.py                      # 15 physics units, ~3 min; with no arguments also the whole-step unit, whose port is not expected to pass the ULP gate
python column.py --mode jax             # one day closed loop
python month_jax.py                     # Fig. 5 (needs the 31-day recording)
python gradients.py fortran:mlleafphotosynthesismod
```

The per-unit JAX gates under `output/port/` were last run with RecastEngine
`main` at `9b2f515` (2026-09-03) and `recast-clm-ml` at `cfb3fce`; the
column, gradient and calibration results under `output/` were made with the
engine at `11512f6` (2026-09-02). Both on jax 0.10.2,
numpy 2.4.6, Python 3.11.16, gfortran 16.1.0 and netCDF-Fortran 4.6.4
(macOS, Apple silicon). The reference Fortran is built by `build/build.sh`
(gfortran `-O2`, topological order from `output/topo_order.txt`).

## License

The scripts and the report are Apache-2.0 (`LICENSE`). The generated code
under `output/` is derived from the upstream Fortran, whose terms are its
authors' (the repository carries no license file). No copy of that Fortran is
in this repository or its history: `output/*/staged/` and the oracle wrappers
are regenerated by `stage.py` and `record.py` from your own clone.
