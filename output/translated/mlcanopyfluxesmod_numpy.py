"""Machine-translated from MLCanopyFluxesMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call mlcanopyfluxes before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
from typing import Any

import numpy as np

from mlcanopyfluxesmod_constants import *  # noqa: F401,F403
from mlcanopyfluxesmod_use_constants import *  # noqa: F401,F403
import abortutils_numpy as _abortutils
import atm2lndtype_numpy as _atm
import atm2lndtype_numpy as _atm2lndtype
import canopystatetype_numpy as _can
import canopystatetype_numpy as _canopystatetype
import clm_time_manager_numpy as _clm
import clm_time_manager_numpy as _clm_time_manager
import clm_varcon_numpy as _clm_varcon
import clm_varctl_numpy as _clm_varctl
import clm_varorb_numpy as _clm_varorb
import clm_varpar_numpy as _clm_varpar
import columntype_numpy as _columntype
import decompmod_numpy as _decompmod
import energyfluxtype_numpy as _ene
import energyfluxtype_numpy as _energyfluxtype
import frictionvelocitymod_numpy as _fri
import frictionvelocitymod_numpy as _frictionvelocitymod
import gridcelltype_numpy as _gri
import gridcelltype_numpy as _gridcelltype
import mlcanopyfluxestype_numpy as _mlc
import mlcanopyfluxestype_numpy as _mlcanopyfluxestype
import mlcanopynitrogenprofilemod_numpy as _mlca
import mlcanopynitrogenprofilemod_numpy as _mlcanopynitrogenprofilemod
import mlcanopyturbulencemod_numpy as _mlcan
import mlcanopyturbulencemod_numpy as _mlcanopyturbulencemod
import mlcanopywatermod_numpy as _mlcano
import mlcanopywatermod_numpy as _mlcanopywatermod
import mlclm_varcon_numpy as _mlclm_varcon
import mlclm_varctl_numpy as _mlclm_varctl
import mlclm_varpar_numpy as _mlclm_varpar
import mlfluxprofilesolutionmod_numpy as _mlf
import mlfluxprofilesolutionmod_numpy as _mlfluxprofilesolutionmod
import mlgetatmforcingmod_numpy as _mlg
import mlgetatmforcingmod_numpy as _mlgetatmforcingmod
import mlinitverticalmod_numpy as _mli
import mlinitverticalmod_numpy as _mlinitverticalmod
import mlleafboundarylayermod_numpy as _mll
import mlleafboundarylayermod_numpy as _mlleafboundarylayermod
import mlleafheatcapacitymod_numpy as _mlle
import mlleafheatcapacitymod_numpy as _mlleafheatcapacitymod
import mlleafphotosynthesismod_numpy as _mllea
import mlleafphotosynthesismod_numpy as _mlleafphotosynthesismod
import mllongwaveradiationmod_numpy as _mllo
import mllongwaveradiationmod_numpy as _mllongwaveradiationmod
import mlplanthydraulicsmod_numpy as _mlp
import mlplanthydraulicsmod_numpy as _mlplanthydraulicsmod
import mlrungekuttamod_numpy as _mlr
import mlrungekuttamod_numpy as _mlrungekuttamod
import mlsolarradiationmod_numpy as _mls
import mlsolarradiationmod_numpy as _mlsolarradiationmod
import mlwatervapormod_numpy as _mlw
import mlwatervapormod_numpy as _mlwatervapormod
import patchtype_numpy as _patchtype
import shr_kind_mod_numpy as _shr_kind_mod
import shr_orb_mod_numpy as _shr
import shr_orb_mod_numpy as _shr_orb_mod
import soilstatetype_numpy as _soi
import soilstatetype_numpy as _soilstatetype
import solarabsorbedtype_numpy as _sol
import solarabsorbedtype_numpy as _solarabsorbedtype
import spmdmod_numpy as _spmdmod
import surfacealbedotype_numpy as _sur
import surfacealbedotype_numpy as _surfacealbedotype
import temperaturetype_numpy as _tem
import temperaturetype_numpy as _temperaturetype
import wateratm2lndbulktype_numpy as _wat
import wateratm2lndbulktype_numpy as _wateratm2lndbulktype
import waterdiagnosticbulktype_numpy as _wate
import waterdiagnosticbulktype_numpy as _waterdiagnosticbulktype
import waterfluxbulktype_numpy as _water
import waterfluxbulktype_numpy as _waterfluxbulktype
import waterstatebulktype_numpy as _waters
import waterstatebulktype_numpy as _waterstatebulktype

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'mlcanopyfluxes': {'kind': 'subroutine', 'args': [{'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'num_exposedvegp', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter_exposedvegp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'atm2lnd_inst', 'dtype': 'UNKNOWN(TYPE(ATM2LND_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'canopystate_inst', 'dtype': 'UNKNOWN(TYPE(CANOPYSTATE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'soilstate_inst', 'dtype': 'UNKNOWN(TYPE(SOILSTATE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'temperature_inst', 'dtype': 'UNKNOWN(TYPE(TEMPERATURE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'waterstatebulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERSTATEBULK_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'waterfluxbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERFLUXBULK_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'energyflux_inst', 'dtype': 'UNKNOWN(TYPE(ENERGYFLUX_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'frictionvel_inst', 'dtype': 'UNKNOWN(TYPE(FRICTIONVEL_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'surfalb_inst', 'dtype': 'UNKNOWN(TYPE(SURFALB_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'solarabs_inst', 'dtype': 'UNKNOWN(TYPE(SOLARABS_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'wateratm2lndbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERATM2LNDBULK_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'waterdiagnosticbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERDIAGNOSTICBULK_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'getclmvar': {'kind': 'subroutine', 'args': [{'name': 'nstep', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'dtime_clm', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'atm2lnd_inst', 'dtype': 'UNKNOWN(TYPE(ATM2LND_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'soilstate_inst', 'dtype': 'UNKNOWN(TYPE(SOILSTATE_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'temperature_inst', 'dtype': 'UNKNOWN(TYPE(TEMPERATURE_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'surfalb_inst', 'dtype': 'UNKNOWN(TYPE(SURFALB_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'wateratm2lndbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERATM2LNDBULK_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'mltimestepfluxintegration': {'kind': 'subroutine', 'args': [{'name': 'nstep_ml', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'num_ml_steps', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'flux_accumulator', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}]}, {'name': 'flux_accumulator_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}]}, {'name': 'flux_accumulator_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'canopyfluxesdiagnostics': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}}

_LIBM_STRICT = os.environ.get("PY_LIBM_STRICT", "1") == "1"
"""Strict libm, on by default.

``np.exp``/``log``/``power`` (npy_math, SIMD) differ from glibc libm by one
ULP. This backend serves the bit-exact gates, so agreement wins; setting
``PY_LIBM_STRICT=0`` buys throughput, and the njit and CUDA backends are the
ones to reach for when throughput is the point.
"""


def _f_vexp(x: Any) -> Any:
    if _LIBM_STRICT:
        return np.array([math.exp(v) for v in np.ravel(x)]).reshape(np.shape(x))
    return np.exp(x)


def _f_vlog(x: Any) -> Any:
    if _LIBM_STRICT:
        return np.array([math.log(v) for v in np.ravel(x)]).reshape(np.shape(x))
    return np.log(x)


def _f_vlog10(x: Any) -> Any:
    if _LIBM_STRICT:
        return np.array([math.log10(v) for v in np.ravel(x)]).reshape(np.shape(x))
    return np.log10(x)


def _f_vpow(a: Any, b: Any) -> Any:
    """array ** : CPython scalar pow == gfortran (libm pow / squaring for
    int exponents); np.power is 1 ULP off either."""
    if _LIBM_STRICT:
        bc = np.broadcast(a, b)
        return np.array([x**y for x, y in bc]).reshape(bc.shape)
    return a**b


def _f_cfold(fn: Any, *args: Any) -> Any:
    """gfortran evaluates constant-argument intrinsics at COMPILE time
    with MPFR (correctly rounded) — that value matches no runtime libm
    (proven: gamma(1.8) differs from BOTH libgfortran and glibc)."""
    import mpmath as mp

    with mp.workprec(200):
        return float(getattr(mp, fn)(*[mp.mpf(float(a)) for a in args]))


def _f_vceil(x: Any) -> Any:
    """Fortran CEILING returns default INTEGER."""
    return np.ceil(x).astype(np.int32)


def _f_vfloor(x: Any) -> Any:
    """Fortran FLOOR returns default INTEGER; np.floor returns float."""
    return np.floor(x).astype(np.int32)


class _FLoopExit(Exception):
    """``EXIT <name>`` naming a DO that is not the innermost one.

    Python's ``break`` leaves one loop, and Fortran's named EXIT leaves the
    one it names. Emitting ``break`` for both is not a shape difference: it
    leaves the *inner* loop and then runs whatever follows it inside the
    outer one, so the program keeps going down a path the Fortran had
    abandoned. The named loop catches this and checks the name, so an EXIT
    crossing two loops passes through the first.
    """


class _FLoopCycle(Exception):
    """``CYCLE <name>`` naming a DO that is not the innermost one.

    The counterpart of ``_FLoopExit``, and the more dangerous of the two: a
    wrong ``continue`` re-runs an inner loop that was supposed to be
    finished, which usually still terminates and still produces numbers.
    """


class _FBlockExit(Exception):
    """``EXIT <name>`` naming an enclosing BLOCK construct.

    A BLOCK is inlined rather than emitted as a scope of its own, so there
    is no Python construct for a ``break`` to leave -- it would bind to
    whatever loop happens to be outside.
    """


class _FGoto(Exception):
    """forward-goto region jump (structured replacement for `goto L`)."""


def _f_ecall(fn: Any, *args: Any, **kw: Any) -> Any:
    """ELEMENTAL procedure broadcast over array actuals: run the scalar
    translation per element (keeps the strict-libm scalar paths and the
    scalar control flow intact). Keywords (optional/want_ sentinels)
    broadcast alongside."""
    return np.vectorize(fn)(*args, **kw)


def _f_copy_out(dst: Any, src: Any) -> None:
    """Copy a callee's returned OUT array into the caller's buffer.

    ``dst[...] = src`` when the shapes agree; when they do not -- a
    ``pcols``-wide buffer receiving an ``ncol``-wide result, or a rank-1
    buffer receiving a section -- the overlap is copied and the rest left as
    it was, which is what Fortran's by-reference OUT did. ``None`` is an
    unsupplied optional, and nothing is written."""
    if dst is None:
        return
    if not isinstance(src, np.ndarray):
        dst[...] = src
        return
    if src.shape == dst.shape:
        dst[...] = src
        return
    if src.ndim == dst.ndim and src.ndim > 1:
        slices = tuple(slice(0, min(s, d)) for s, d in zip(src.shape, dst.shape, strict=True))
        dst[slices] = src[slices]
    else:
        n = min(src.size, dst.size)
        dst.ravel()[:n] = src.ravel()[:n]


def _f_rstep(lo: Any, hi: Any, st: Any) -> Any:
    """Fortran lo:hi:st (st<0, inclusive, 1-based) -> python slice; the
    exclusive stop edge underflows at hi==1, which needs None."""
    return slice(lo - 1, hi - 2 if hi >= 2 else None, st)


def _f_rstep_lb(lo: Any, hi: Any, st: Any, lb: Any) -> Any:
    """Fortran lo:hi:st (st<0, inclusive) with declared lower bound lb.

    Either edge may be None: Fortran lets a section leave one implied."""
    start = None if lo is None else lo - lb
    stop = None
    if hi is not None:
        index = hi - lb
        stop = index - 1 if index >= 1 else None
    return slice(start, stop, st)


def _f_vdot(a: Any, b: Any) -> Any:
    """Fortran DOT_PRODUCT accumulates in order; np.dot (BLAS/pairwise)
    rounds differently."""
    if _LIBM_STRICT:
        s = 0.0
        # Unchecked on purpose: this is the emitted runtime, and it has
        # been through bit-exact gates in this form. A length mismatch is
        # invalid Fortran that never reaches here.
        for x, y in zip(np.ravel(a), np.ravel(b)):  # noqa: B905
            s += x * y
        return s
    return np.dot(a, b)


def _fstr_eq(a: str, b: str) -> bool:
    """Fortran character equality: pad shorter operand with blanks."""
    return a.rstrip(" ") == b.rstrip(" ")


class _new_derived:  # noqa: N801  (the emitted name; not a class the engine exposes)
    """Fortran derived-type local: attribute container (components are
    attached by translated allocate statements)."""

    pass


def _copy_derived(obj: Any) -> Any:
    """Fortran derived-type assignment is a DEEP copy (incl. array
    components); python name binding is not."""
    import copy

    return copy.deepcopy(obj)


def _f_trim(s: str) -> str:
    """Fortran TRIM: strip trailing blanks only."""
    return s.rstrip(" ")


def _f_len_trim(s: str) -> int:
    return len(s.rstrip(" "))


def _f_adjustl(s: str) -> str:
    """Fortran ADJUSTL keeps length (pads right)."""
    return s.lstrip(" ").ljust(len(s))


def _f_min(*xs: Any) -> Any:
    """gfortran MIN (SSE minsd order, MEASURED): per fold step the FIRST
    operand's NaN is absorbed, the second's propagates:
    min(NaN,0)=0 but min(0,NaN)=NaN. Python's builtin min returns the
    first arg on NaN — a one-sided-NaN behavior trap."""
    r = xs[0]
    for b in xs[1:]:
        r = b if (r != r) else (r if r < b else b)
    return r


def _f_max(*xs: Any) -> Any:
    r = xs[0]
    for b in xs[1:]:
        r = b if (r != r) else (r if r > b else b)
    return r


def _f_vmin(a: Any, b: Any) -> Any:
    """elementwise gfortran MIN semantics (see _f_min)."""
    return np.where(np.isnan(a), b, np.where(a < b, a, b))


def _f_vmax(a: Any, b: Any) -> Any:
    return np.where(np.isnan(a), b, np.where(a > b, a, b))


def _f_nint(x: Any) -> Any:
    """Fortran NINT: round half away from zero (not banker's rounding).
    Python round() uses banker's rounding: round(0.5)=0, round(2.5)=2.
    Fortran NINT: NINT(0.5)=1, NINT(2.5)=3."""
    if isinstance(x, (float, np.floating)):
        return np.int32(math.floor(x + 0.5)) if x >= 0 else np.int32(math.ceil(x - 0.5))
    return np.int32(x)


def _f_sign(a: Any, b: Any) -> Any:
    """Fortran SIGN(a,b). Real b: IEEE copysign (gfortran distinguishes
    -0.0 -> -|a|). Integer b: value compare, b == 0 -> +|a| (differs from
    copysign there — the classic port trap)."""
    if isinstance(b, (float, np.floating)):
        return math.copysign(abs(a), b)
    return abs(a) if b >= 0 else -abs(a)


def _f_mod(a: Any, p: Any) -> Any:
    """Fortran MOD(a,p) = a - int(a/p)*p (truncated, sign follows a).
    Python % floors (sign follows p) — not equivalent for negatives."""
    return a - int(a / p) * p


def _f_int_div(a: Any, b: Any) -> Any:
    """Fortran integer division truncates toward zero; Python // floors."""
    return int(a / b)


def _f_list_write(*items: Any) -> Any:
    """gfortran list-directed internal WRITE shim.

    Byte-exact against reference probes: a record starts with one blank,
    strings print verbatim, ``int32`` becomes I12 plus a blank separator,
    ``real(8)`` becomes G25.17E3 plus a blank.

    Percent formatting throughout, deliberately. The point of this function
    is to reproduce another language's output byte for byte, and ``%`` is
    the spelling whose width, precision and sign rules match the Fortran
    edit descriptors it is emulating. Restating them in ``format`` would be
    a re-derivation of something already validated against real output.
    """
    out = " "
    for it in items:
        if isinstance(it, str):
            out += it
        elif isinstance(it, (int, np.integer)):
            out += "%12d " % int(it)  # noqa: UP031
        else:
            v = float(it)
            av = abs(v)
            if v == 0.0 or (0.1 <= av < 1e17):
                int_digits = 0 if av < 1.0 else len(str(int(av)))
                out += "%21.*f" % (17 - int_digits, v) + " " * 6  # noqa: UP031
            else:
                mant, ex = ("%.16E" % v).split("E")  # noqa: UP031
                out += ("%sE%+04d" % (mant, int(ex))).rjust(26) + " "  # noqa: UP031
    return out


def _f_unpack(vector: Any, mask: Any, field: Any) -> Any:
    """Fortran UNPACK: scatter vector elements into field where mask is True."""
    result = field.copy()
    result[mask] = vector[: np.count_nonzero(mask)]
    return result


def _f_eoshift(array: Any, shift: Any, axis: Any = 0) -> Any:
    """Fortran EOSHIFT: shift and fill with zeros (no wrap-around)."""
    result = np.zeros_like(array)
    n = array.shape[axis]
    s = int(shift)
    if s > 0:
        slc_src = [slice(None)] * array.ndim
        slc_dst = [slice(None)] * array.ndim
        slc_src[axis] = slice(s, None)
        slc_dst[axis] = slice(None, n - s)
        result[tuple(slc_dst)] = array[tuple(slc_src)]
    elif s < 0:
        slc_src = [slice(None)] * array.ndim
        slc_dst = [slice(None)] * array.ndim
        slc_src[axis] = slice(None, s)
        slc_dst[axis] = slice(-s, None)
        result[tuple(slc_dst)] = array[tuple(slc_src)]
    else:
        result[...] = array
    return result


def _f_index(string: str, substring: str) -> int:
    """Fortran INDEX: 1-based position, 0 if not found."""
    p = string.find(substring)
    return p + 1 if p >= 0 else 0


def _f_huge(x: Any) -> Any:
    """Fortran HUGE: largest representable value of same type."""
    if isinstance(x, (float, np.floating)):
        return np.finfo(np.float64).max
    return np.iinfo(np.int32).max


def _f_tiny(x: Any) -> Any:
    """Fortran TINY: smallest positive normalized value."""
    return np.finfo(np.float64).tiny


def _f_epsilon(x: Any) -> Any:
    """Fortran EPSILON: smallest difference from 1.0 of same type."""
    return np.finfo(np.float64).eps


def _f_modulo(a: Any, p: Any) -> Any:
    """Fortran MODULO(a,p): result has sign of p (floored). Python % semantics."""
    return a % p


def _f_iand(a: Any, b: Any) -> Any:
    return int(a) & int(b)


def _f_ior(a: Any, b: Any) -> Any:
    return int(a) | int(b)


def _f_ieor(a: Any, b: Any) -> Any:
    return int(a) ^ int(b)


def _f_ishft(i: Any, shift: Any) -> Any:
    """Fortran ISHFT: positive shift = left, negative = right."""
    s = int(shift)
    return (int(i) << s) if s >= 0 else (int(i) >> (-s))


def _f_scan(string: str, set_chars: str) -> int:
    """Fortran SCAN: 1-based index of first char in set, 0 if none."""
    for i, c in enumerate(string):
        if c in set_chars:
            return i + 1
    return 0


def _f_kind(x: Any) -> Any:
    if isinstance(x, (float, np.floating)):
        return 8
    if isinstance(x, (int, np.integer)):
        return 4
    return 1


def _f_precision(x: Any) -> Any:
    return 15


def _f_transfer(source: Any, mold: Any) -> Any:
    """Fortran TRANSFER: reinterpret bit pattern."""
    src = np.array(source)
    viewed = src.view(np.array(mold).dtype)
    if hasattr(mold, "__len__"):
        return viewed.reshape(np.shape(mold))
    return viewed.flat[0]


def _f_is_iostat_end(stat: int) -> bool:
    return stat < 0


def _f_lbound(arr: Any, dim: Any = None) -> Any:
    """Fortran LBOUND is always 1 for standard arrays."""
    if dim is not None:
        return 1
    return np.ones(arr.ndim, dtype=np.int32)


def _f_c_loc(x: Any) -> Any:
    return id(x)


def _f_dim(x: Any, y: Any) -> Any:
    """Fortran DIM(x,y) = max(x-y, 0)."""
    return max(x - y, 0)


def _f_mvbits(from_val: Any, frompos: Any, length: Any, to_val: Any, topos: Any) -> Any:
    """Fortran MVBITS: copy bits. Returns modified to_val."""
    mask = (1 << length) - 1
    bits = (int(from_val) >> int(frompos)) & mask
    to_int = int(to_val)
    to_int &= ~(mask << int(topos))
    to_int |= bits << int(topos)
    return type(to_val)(to_int)


def _f_verf(x: Any) -> Any:
    from scipy.special import erf as _sp_erf

    return _sp_erf(x)


def _f_verfc(x: Any) -> Any:
    from scipy.special import erfc as _sp_erfc

    return _sp_erfc(x)


class _FIntrinsicModule:
    """The public names of one Fortran intrinsic module, as a namespace.

    ``USE ISO_FORTRAN_ENV`` names a module the standard (or the compiler)
    provides rather than one sitting in the tree, so there is no companion to
    translate and nothing to import. Binding such a USE the way an ordinary
    one is bound emits ``import iso_fortran_env_numpy``, a module that can
    never exist, and the translated file fails at import before any number is
    wrong. The emitter binds it to one of the objects below instead, and
    because they are part of this runtime they are already in the generated
    file -- no import line is emitted for them at all.
    """

    def __init__(self, **names: Any) -> None:
        self.__dict__.update(names)


def _f_ieee_value(x: Any, cls: Any) -> Any:
    """``IEEE_VALUE(X, CLASS)``: the class constants are spelled as themselves."""
    return {
        "ieee_positive_inf": np.inf,
        "ieee_negative_inf": -np.inf,
        "ieee_quiet_nan": np.nan,
        "ieee_signaling_nan": np.nan,
        "ieee_positive_zero": 0.0,
        "ieee_negative_zero": -0.0,
    }[cls]


# The named constants of these modules are kind *numbers* -- ``real64`` is 8,
# not a dtype -- because that is what the source reads when it compares one
# (``if (kind(x) /= real64)``). The frontend has a table of its own mapping the
# same names to dtypes for a declaration; the two are different questions.
_iso_fortran_env = _FIntrinsicModule(
    int8=np.int32(1),
    int16=np.int32(2),
    int32=np.int32(4),
    int64=np.int32(8),
    real32=np.int32(4),
    real64=np.int32(8),
    real128=np.int32(16),
    input_unit=np.int32(5),
    output_unit=np.int32(6),
    error_unit=np.int32(0),
    iostat_end=np.int32(-1),
    iostat_eor=np.int32(-2),
    numeric_storage_size=np.int32(32),
    character_storage_size=np.int32(8),
    file_storage_size=np.int32(8),
)

# ``c_null_char`` and ``c_new_line`` are the characters, not the two-character
# escapes that spell them in source: ``C_NULL_CHAR`` is ``ACHAR(0)``, and a
# string terminated with a literal backslash-zero is not terminated at all.
_iso_c_binding = _FIntrinsicModule(
    c_int=np.int32(4),
    c_short=np.int32(2),
    c_long=np.int32(8),
    c_long_long=np.int32(8),
    c_size_t=np.int32(8),
    c_int8_t=np.int32(1),
    c_int16_t=np.int32(2),
    c_int32_t=np.int32(4),
    c_int64_t=np.int32(8),
    c_float=np.int32(4),
    c_double=np.int32(8),
    c_long_double=np.int32(16),
    c_float_complex=np.int32(4),
    c_double_complex=np.int32(8),
    c_bool=np.int32(1),
    c_char=np.int32(1),
    c_null_char=chr(0),
    c_new_line=chr(10),
    c_carriage_return=chr(13),
    c_horizontal_tab=chr(9),
    c_null_ptr=None,
    c_loc=_f_c_loc,
)

_ieee_arithmetic = _FIntrinsicModule(
    ieee_is_nan=np.isnan,
    ieee_is_finite=np.isfinite,
    ieee_is_negative=np.signbit,
    ieee_is_normal=lambda x: np.isfinite(x) & (x != 0.0),
    ieee_value=_f_ieee_value,
    ieee_support_datatype=lambda *_a: True,
    ieee_positive_inf="ieee_positive_inf",
    ieee_negative_inf="ieee_negative_inf",
    ieee_quiet_nan="ieee_quiet_nan",
    ieee_signaling_nan="ieee_signaling_nan",
    ieee_positive_zero="ieee_positive_zero",
    ieee_negative_zero="ieee_negative_zero",
)

_ieee_exceptions = _FIntrinsicModule()
_ieee_features = _FIntrinsicModule()

# The translated module is serial, so the OpenMP enquiries answer as the
# runtime library does outside a parallel region. A translation that reported
# more than one thread would be describing a program that is not running.
_omp_lib = _FIntrinsicModule(
    omp_get_num_threads=lambda: np.int32(1),
    omp_get_max_threads=lambda: np.int32(1),
    omp_get_thread_num=lambda: np.int32(0),
    omp_get_num_procs=lambda: np.int32(1),
    omp_in_parallel=lambda: False,
    omp_get_wtime=lambda: 0.0,
)
_omp_lib_kinds = _FIntrinsicModule()
_openacc = _FIntrinsicModule(acc_get_num_devices=lambda *_a: np.int32(0))

def _make_atm2lnd_type():
    """factory for type(atm2lnd_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.forc_u_grc = None
    o.forc_v_grc = None
    o.forc_pco2_grc = None
    o.forc_po2_grc = None
    o.forc_solad_downscaled_col = None
    o.forc_solai_grc = None
    o.forc_t_downscaled_col = None
    o.forc_pbot_downscaled_col = None
    o.forc_lwrad_downscaled_col = None
    return o

def _make_canopystate_type():
    """factory for type(canopystate_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.frac_veg_nosno_patch = None
    o.elai_patch = None
    o.esai_patch = None
    o.htop_patch = None
    return o

def _make_column_type():
    """factory for type(column_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.snl = None
    o.dz = None
    o.z = None
    o.zi = None
    o.nbedrock = None
    return o

def _make_energyflux_type():
    """factory for type(energyflux_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.eflx_sh_tot_patch = None
    o.eflx_lh_tot_patch = None
    o.eflx_lwrad_out_patch = None
    o.taux_patch = None
    o.tauy_patch = None
    return o

def _make_frictionvel_type():
    """factory for type(frictionvel_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.forc_hgt_u_patch = None
    o.u10_clm_patch = None
    o.fv_patch = None
    return o

def _make_gridcell_type():
    """factory for type(gridcell_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.latdeg = None
    o.londeg = None
    return o

def _make_patch_type():
    """factory for type(patch_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.column = None
    o.gridcell = None
    o.itype = None
    return o

def _make_soilstate_type():
    """factory for type(soilstate_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.cellorg_col = None
    o.cellsand_col = None
    o.cellclay_col = None
    o.hksat_col = None
    o.hk_l_col = None
    o.smp_l_col = None
    o.bsw_col = None
    o.watsat_col = None
    o.sucsat_col = None
    o.dsl_col = None
    o.soilresis_col = None
    o.thk_col = None
    o.tkmg_col = None
    o.tkdry_col = None
    o.csol_col = None
    o.rootfr_patch = None
    return o

def _make_solarabs_type():
    """factory for type(solarabs_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.fsa_patch = None
    return o

def _make_surfalb_type():
    """factory for type(surfalb_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.coszen_col = None
    o.albd_patch = None
    o.albi_patch = None
    o.albgrd_col = None
    o.albgri_col = None
    return o

def _make_temperature_type():
    """factory for type(temperature_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.t_soisno_col = None
    o.t_a10_patch = None
    o.t_ref2m_patch = None
    return o

def _make_wateratm2lndbulk_type():
    """factory for type(wateratm2lndbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.forc_q_downscaled_col = None
    o.forc_rain_downscaled_col = None
    o.forc_snow_downscaled_col = None
    return o

def _make_waterdiagnosticbulk_type():
    """factory for type(waterdiagnosticbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.q_ref2m_patch = None
    o.frac_sno_eff_col = None
    o.bw_col = None
    return o

def _make_waterfluxbulk_type():
    """factory for type(waterfluxbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.qflx_evap_tot_patch = None
    return o

def _make_waterstatebulk_type():
    """factory for type(waterstatebulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.h2osoi_liq_col = None
    o.h2osoi_ice_col = None
    o.h2osoi_vol_col = None
    o.h2osfc_col = None
    return o

def _make_mlcanopy_type():
    """factory for type(mlcanopy_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.ztop_canopy = None
    o.zbot_canopy = None
    o.lai_canopy = None
    o.sai_canopy = None
    o.root_biomass_canopy = None
    o.pbeta_lai_canopy = None
    o.pbeta_sai_canopy = None
    o.zref_forcing = None
    o.tref_forcing = None
    o.tref_bef_forcing = None
    o.tref_cur_forcing = None
    o.tref_next_forcing = None
    o.qref_forcing = None
    o.qref_bef_forcing = None
    o.qref_cur_forcing = None
    o.qref_next_forcing = None
    o.uref_forcing = None
    o.uref_bef_forcing = None
    o.uref_cur_forcing = None
    o.uref_next_forcing = None
    o.pref_forcing = None
    o.pref_bef_forcing = None
    o.pref_cur_forcing = None
    o.pref_next_forcing = None
    o.co2ref_forcing = None
    o.co2ref_bef_forcing = None
    o.co2ref_cur_forcing = None
    o.co2ref_next_forcing = None
    o.o2ref_forcing = None
    o.swskyb_forcing = None
    o.swskyb_bef_forcing = None
    o.swskyb_cur_forcing = None
    o.swskyb_next_forcing = None
    o.swskyd_forcing = None
    o.swskyd_bef_forcing = None
    o.swskyd_cur_forcing = None
    o.swskyd_next_forcing = None
    o.lwsky_forcing = None
    o.lwsky_bef_forcing = None
    o.lwsky_cur_forcing = None
    o.lwsky_next_forcing = None
    o.qflx_rain_forcing = None
    o.qflx_snow_forcing = None
    o.tacclim_forcing = None
    o.eref_forcing = None
    o.thref_forcing = None
    o.thvref_forcing = None
    o.rhoair_forcing = None
    o.rhomol_forcing = None
    o.mmair_forcing = None
    o.cpair_forcing = None
    o.solar_zen_forcing = None
    o.swveg_canopy = None
    o.swvegsun_canopy = None
    o.swvegsha_canopy = None
    o.lwveg_canopy = None
    o.lwvegsun_canopy = None
    o.lwvegsha_canopy = None
    o.shveg_canopy = None
    o.shvegsun_canopy = None
    o.shvegsha_canopy = None
    o.lhveg_canopy = None
    o.lhvegsun_canopy = None
    o.lhvegsha_canopy = None
    o.etveg_canopy = None
    o.etvegsun_canopy = None
    o.etvegsha_canopy = None
    o.trveg_canopy = None
    o.evveg_canopy = None
    o.gppveg_canopy = None
    o.gppvegsun_canopy = None
    o.gppvegsha_canopy = None
    o.vcmax25veg_canopy = None
    o.vcmax25sun_canopy = None
    o.vcmax25sha_canopy = None
    o.gsveg_canopy = None
    o.gsvegsun_canopy = None
    o.gsvegsha_canopy = None
    o.windveg_canopy = None
    o.windvegsun_canopy = None
    o.windvegsha_canopy = None
    o.tlveg_canopy = None
    o.tlvegsun_canopy = None
    o.tlvegsha_canopy = None
    o.taveg_canopy = None
    o.tavegsun_canopy = None
    o.tavegsha_canopy = None
    o.laisun_canopy = None
    o.laisha_canopy = None
    o.albcan_canopy = None
    o.lwup_canopy = None
    o.rnet_canopy = None
    o.shflx_canopy = None
    o.lhflx_canopy = None
    o.etflx_canopy = None
    o.stflx_air_canopy = None
    o.stflx_veg_canopy = None
    o.ustar_canopy = None
    o.gac_to_hc_canopy = None
    o.qflx_intr_canopy = None
    o.qflx_tflrain_canopy = None
    o.qflx_tflsnow_canopy = None
    o.uaf_canopy = None
    o.taf_canopy = None
    o.qaf_canopy = None
    o.fracminlwp_canopy = None
    o.obu_canopy = None
    o.beta_canopy = None
    o.prsc_canopy = None
    o.lc_canopy = None
    o.zdisp_canopy = None
    o.z0m_canopy = None
    o.g0_canopy = None
    o.g1_canopy = None
    o.albsoib_soil = None
    o.albsoid_soil = None
    o.swsoi_soil = None
    o.lwsoi_soil = None
    o.rnsoi_soil = None
    o.shsoi_soil = None
    o.lhsoi_soil = None
    o.etsoi_soil = None
    o.gsoi_soil = None
    o.tg_soil = None
    o.tg_bef_soil = None
    o.dtg_soil = None
    o.eg_soil = None
    o.rhg_soil = None
    o.gac0_soil = None
    o.soil_t_soil = None
    o.soil_dz_soil = None
    o.soil_tk_soil = None
    o.soilres_soil = None
    o.btran_soil = None
    o.psis_soil = None
    o.rsoil_soil = None
    o.soil_et_loss_soil = None
    o.ncan_canopy = None
    o.ntop_canopy = None
    o.nbot_canopy = None
    o.dlai_frac_profile = None
    o.dsai_frac_profile = None
    o.dlai_profile = None
    o.dsai_profile = None
    o.dpai_profile = None
    o.zs_profile = None
    o.zw_profile = None
    o.dz_profile = None
    o.vcmax25_profile = None
    o.jmax25_profile = None
    o.kp25_profile = None
    o.rd25_profile = None
    o.cpleaf_profile = None
    o.fracsun_profile = None
    o.kb_profile = None
    o.tb_profile = None
    o.td_profile = None
    o.tbi_profile = None
    o.swbeam_profile = None
    o.swupw_profile = None
    o.swdwn_profile = None
    o.lwupw_profile = None
    o.lwdwn_profile = None
    o.swsrc_profile = None
    o.lwsrc_profile = None
    o.rnsrc_profile = None
    o.stsrc_profile = None
    o.shsrc_profile = None
    o.lhsrc_profile = None
    o.etsrc_profile = None
    o.trsrc_profile = None
    o.evsrc_profile = None
    o.fco2src_profile = None
    o.wind_profile = None
    o.tair_profile = None
    o.eair_profile = None
    o.cair_profile = None
    o.tair_bef_profile = None
    o.eair_bef_profile = None
    o.cair_bef_profile = None
    o.dtair_profile = None
    o.deair_profile = None
    o.wind_data_profile = None
    o.tair_data_profile = None
    o.eair_data_profile = None
    o.shair_profile = None
    o.etair_profile = None
    o.stair_profile = None
    o.mflx_profile = None
    o.gac_profile = None
    o.kc_eddy_profile = None
    o.swleaf_mean_profile = None
    o.lwleaf_mean_profile = None
    o.rnleaf_mean_profile = None
    o.stleaf_mean_profile = None
    o.shleaf_mean_profile = None
    o.lhleaf_mean_profile = None
    o.etleaf_mean_profile = None
    o.trleaf_mean_profile = None
    o.evleaf_mean_profile = None
    o.fco2_mean_profile = None
    o.apar_mean_profile = None
    o.gs_mean_profile = None
    o.tleaf_mean_profile = None
    o.lwp_mean_profile = None
    o.lsc_profile = None
    o.h2ocan_profile = None
    o.h2ocan_bef_profile = None
    o.dh2ocan_profile = None
    o.fwet_profile = None
    o.fdry_profile = None
    o.tleaf_leaf = None
    o.tleaf_bef_leaf = None
    o.dtleaf_leaf = None
    o.tleaf_hist_leaf = None
    o.swleaf_leaf = None
    o.lwleaf_leaf = None
    o.rnleaf_leaf = None
    o.stleaf_leaf = None
    o.shleaf_leaf = None
    o.lhleaf_leaf = None
    o.trleaf_leaf = None
    o.evleaf_leaf = None
    o.gbh_leaf = None
    o.gbv_leaf = None
    o.gbc_leaf = None
    o.vcmax25_leaf = None
    o.jmax25_leaf = None
    o.kp25_leaf = None
    o.rd25_leaf = None
    o.kc_leaf = None
    o.ko_leaf = None
    o.cp_leaf = None
    o.vcmax_leaf = None
    o.jmax_leaf = None
    o.kp_leaf = None
    o.ceair_leaf = None
    o.leaf_esat_leaf = None
    o.apar_leaf = None
    o.je_leaf = None
    o.ac_leaf = None
    o.aj_leaf = None
    o.ap_leaf = None
    o.agross_leaf = None
    o.anet_leaf = None
    o.rd_leaf = None
    o.ci_leaf = None
    o.cs_leaf = None
    o.lwp_leaf = None
    o.lwp_bef_leaf = None
    o.dlwp_leaf = None
    o.lwp_hist_leaf = None
    o.hs_leaf = None
    o.vpd_leaf = None
    o.gs_leaf = None
    o.gspot_leaf = None
    return o


def mlcanopyfluxes(bounds, num_exposedvegp, filter_exposedvegp, atm2lnd_inst, canopystate_inst, soilstate_inst, temperature_inst, waterstatebulk_inst, waterfluxbulk_inst, energyflux_inst, frictionvel_inst, surfalb_inst, solarabs_inst, mlcanopy_inst, wateratm2lndbulk_inst, waterdiagnosticbulk_inst):
    """L51-L694 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    num_mlcan = 0
    # filter_mlcan: array prologue skipped (dim expr 'bounds % endp - bounds % begp + 1') — first use will AgentQueue
    fp = 0
    p = 0
    c = 0
    g = 0
    ic = 0
    nstep = 0
    num_ml_steps = 0
    nstep_ml = 0
    dtime_clm = 0.0
    curr_calday_end = 0.0
    curr_calday_beg = 0.0
    calday_interp_bef = 0.0
    calday_interp_cur = 0.0
    calday_interp_next = 0.0
    calday_interp_ml = 0.0
    totpai = 0.0
    # flux_accumulator: array prologue skipped (dim expr 'bounds % endp') — first use will AgentQueue
    # flux_accumulator_profile: array prologue skipped (dim expr 'bounds % endp') — first use will AgentQueue
    # flux_accumulator_leaf: array prologue skipped (dim expr 'bounds % endp') — first use will AgentQueue
    irk = 0
    nrk_steps = 0
    ark = np.empty((NRK, NRK,), dtype=np.float64)
    brk = np.empty((NRK,), dtype=np.float64)
    crk = np.empty((NRK,), dtype=np.float64)
    # B001 <- L135-L693
    elai = canopystate_inst.elai_patch
    esai = canopystate_inst.esai_patch
    smp_l = soilstate_inst.smp_l_col
    t_soisno = temperature_inst.t_soisno_col
    eflx_lh_tot = energyflux_inst.eflx_lh_tot_patch
    eflx_sh_tot = energyflux_inst.eflx_sh_tot_patch
    eflx_lwrad_out = energyflux_inst.eflx_lwrad_out_patch
    taux = energyflux_inst.taux_patch
    tauy = energyflux_inst.tauy_patch
    fv = frictionvel_inst.fv_patch
    u10_clm = frictionvel_inst.u10_clm_patch
    fsa = solarabs_inst.fsa_patch
    albd = surfalb_inst.albd_patch
    albi = surfalb_inst.albi_patch
    t_ref2m = temperature_inst.t_ref2m_patch
    qflx_evap_tot = waterfluxbulk_inst.qflx_evap_tot_patch
    q_ref2m = waterdiagnosticbulk_inst.q_ref2m_patch
    zref = mlcanopy_inst.zref_forcing
    tref_bef = mlcanopy_inst.tref_bef_forcing
    tref_cur = mlcanopy_inst.tref_cur_forcing
    qref_bef = mlcanopy_inst.qref_bef_forcing
    qref_cur = mlcanopy_inst.qref_cur_forcing
    uref_bef = mlcanopy_inst.uref_bef_forcing
    uref_cur = mlcanopy_inst.uref_cur_forcing
    pref_bef = mlcanopy_inst.pref_bef_forcing
    pref_cur = mlcanopy_inst.pref_cur_forcing
    co2ref_bef = mlcanopy_inst.co2ref_bef_forcing
    co2ref_cur = mlcanopy_inst.co2ref_cur_forcing
    swskyb_bef = mlcanopy_inst.swskyb_bef_forcing
    swskyb_cur = mlcanopy_inst.swskyb_cur_forcing
    swskyd_bef = mlcanopy_inst.swskyd_bef_forcing
    swskyd_cur = mlcanopy_inst.swskyd_cur_forcing
    lwsky_bef = mlcanopy_inst.lwsky_bef_forcing
    lwsky_cur = mlcanopy_inst.lwsky_cur_forcing
    ncan = mlcanopy_inst.ncan_canopy
    lai = mlcanopy_inst.lai_canopy
    sai = mlcanopy_inst.sai_canopy
    swveg = mlcanopy_inst.swveg_canopy
    lwup = mlcanopy_inst.lwup_canopy
    shflx = mlcanopy_inst.shflx_canopy
    lhflx = mlcanopy_inst.lhflx_canopy
    etflx = mlcanopy_inst.etflx_canopy
    ustar = mlcanopy_inst.ustar_canopy
    swsoi = mlcanopy_inst.swsoi_soil
    lwsoi = mlcanopy_inst.lwsoi_soil
    rnsoi = mlcanopy_inst.rnsoi_soil
    tg = mlcanopy_inst.tg_soil
    tg_bef = mlcanopy_inst.tg_bef_soil
    rhg = mlcanopy_inst.rhg_soil
    dlai = mlcanopy_inst.dlai_profile
    dsai = mlcanopy_inst.dsai_profile
    dpai = mlcanopy_inst.dpai_profile
    dlai_frac = mlcanopy_inst.dlai_frac_profile
    dsai_frac = mlcanopy_inst.dsai_frac_profile
    fracsun = mlcanopy_inst.fracsun_profile
    tair = mlcanopy_inst.tair_profile
    tair_bef = mlcanopy_inst.tair_bef_profile
    eair = mlcanopy_inst.eair_profile
    eair_bef = mlcanopy_inst.eair_bef_profile
    cair = mlcanopy_inst.cair_profile
    cair_bef = mlcanopy_inst.cair_bef_profile
    h2ocan = mlcanopy_inst.h2ocan_profile
    h2ocan_bef = mlcanopy_inst.h2ocan_bef_profile
    swleaf = mlcanopy_inst.swleaf_leaf
    lwleaf = mlcanopy_inst.lwleaf_leaf
    rnleaf = mlcanopy_inst.rnleaf_leaf
    tleaf = mlcanopy_inst.tleaf_leaf
    tleaf_bef = mlcanopy_inst.tleaf_bef_leaf
    tleaf_hist = mlcanopy_inst.tleaf_hist_leaf
    lwp = mlcanopy_inst.lwp_leaf
    lwp_bef = mlcanopy_inst.lwp_bef_leaf
    lwp_hist = mlcanopy_inst.lwp_hist_leaf
    nstep = _clm.get_nstep()
    dtime_clm = _clm.get_step_size()
    curr_calday_end = _clm.get_curr_calday(offset=0)
    curr_calday_beg = _clm.get_curr_calday(offset=(-int(dtime_clm)))
    if (MET_TYPE == 0):
        calday_interp_cur = 0.0
        calday_interp_bef = 0.0
        calday_interp_next = 0.0
    elif (MET_TYPE == 2):
        raise RuntimeError('endrun')  # endrun (infra stub)
        calday_interp_cur = curr_calday_end
        calday_interp_bef = (calday_interp_cur - (dtime_clm / F_86400P))
        calday_interp_next = 0.0
    elif (MET_TYPE == I_3):
        calday_interp_cur = (0.5 * ((curr_calday_end + curr_calday_beg)))
        calday_interp_bef = (calday_interp_cur - (dtime_clm / F_86400P))
        calday_interp_next = (calday_interp_cur + (dtime_clm / F_86400P))
    num_ml_steps = int((dtime_clm / DTIME_ML))
    num_mlcan = 0
    for fp in range(1, num_exposedvegp + 1):
        p = filter_exposedvegp[fp - 1]
        g = _patchtype.patch.gridcell[fp - 1]
        num_mlcan = (num_mlcan + 1)
        filter_mlcan[num_mlcan - 1] = p
    ML_VERT_INIT = 0
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        if (zref[p - 1] == SPVAL):
            ML_VERT_INIT = 1
    if (ML_VERT_INIT == 1):
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
        mlcanopy_inst = _mli.getpadparameters(num_mlcan, filter_mlcan)
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
        mlcanopy_inst = _mli.initverticalstructure(bounds, num_mlcan, filter_mlcan, canopystate_inst, frictionvel_inst)
        mlcanopy_inst = _mli.initverticalprofiles(num_mlcan, filter_mlcan, atm2lnd_inst, wateratm2lndbulk_inst, mlcanopy_inst)
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
        _out = _mlr.rungekuttaini()
        _f_copy_out(ark, _out[0])
        _f_copy_out(brk, _out[1])
        _f_copy_out(crk, _out[2])
    mlcanopy_inst = getclmvar(nstep, dtime_clm, num_mlcan, filter_mlcan, atm2lnd_inst, soilstate_inst, temperature_inst, surfalb_inst, wateratm2lndbulk_inst, mlcanopy_inst)
    if (ML_VERT_INIT == 1):
        for fp in range(1, num_mlcan + 1):
            p = filter_mlcan[fp - 1]
            uref_bef[p - 1] = uref_cur[p - 1]
            tref_bef[p - 1] = tref_cur[p - 1]
            qref_bef[p - 1] = qref_cur[p - 1]
            pref_bef[p - 1] = pref_cur[p - 1]
            co2ref_bef[p - 1] = co2ref_cur[p - 1]
            swskyb_bef[p - 1, IVIS - 1] = swskyb_cur[p - 1, IVIS - 1]
            swskyb_bef[p - 1, INIR - 1] = swskyb_cur[p - 1, INIR - 1]
            swskyd_bef[p - 1, IVIS - 1] = swskyd_cur[p - 1, IVIS - 1]
            swskyd_bef[p - 1, INIR - 1] = swskyd_cur[p - 1, INIR - 1]
            lwsky_bef[p - 1] = lwsky_cur[p - 1]
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        lai[p - 1] = elai[p - 1]
        sai[p - 1] = esai[p - 1]
        for ic in range(1, ncan[p - 1] + 1):
            dlai[p - 1, ic - 1] = (dlai_frac[p - 1, ic - 1] * lai[p - 1])
            dsai[p - 1, ic - 1] = (dsai_frac[p - 1, ic - 1] * sai[p - 1])
            dpai[p - 1, ic - 1] = (dlai[p - 1, ic - 1] + dsai[p - 1, ic - 1])
        totpai = np.sum(dpai[p - 1, 0:ncan[p - 1]])
        if (abs((totpai - ((lai[p - 1] + sai[p - 1])))) > F_1PEM06):
            raise RuntimeError('endrun')  # endrun (infra stub)
    mlcanopy_inst = _mlp.soilresistance(num_mlcan, filter_mlcan, soilstate_inst, waterstatebulk_inst, mlcanopy_inst)
    mlcanopy_inst = _mlp.plantresistance(num_mlcan, filter_mlcan, mlcanopy_inst)
    mlcanopy_inst = _mlle.leafheatcapacity(num_mlcan, filter_mlcan, mlcanopy_inst)
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        c = _patchtype.patch.column[p - 1]
        rhg[p - 1] = math.exp(((((GRAV * MMH2O) * smp_l[c - 1, 0]) * F_1PEM03) / ((RGAS * t_soisno[c - 1, 0]))))
    for nstep_ml in range(1, num_ml_steps + 1):
        try:  # forward-goto region (label 100)
            if (MET_TYPE == 0) or (MET_TYPE == 2):
                calday_interp_ml = (curr_calday_beg + (np.float64(nstep_ml) * ((DTIME_ML / F_86400P))))
            elif (MET_TYPE == I_3):
                calday_interp_ml = (curr_calday_beg + (((np.float64(nstep_ml) - 0.5)) * ((DTIME_ML / F_86400P))))
            for fp in range(1, num_mlcan + 1):
                p = filter_mlcan[fp - 1]
                tg_bef[p - 1] = tg[p - 1]
                for ic in range(1, ncan[p - 1] + 1):
                    tair_bef[p - 1, ic - 1] = tair[p - 1, ic - 1]
                    eair_bef[p - 1, ic - 1] = eair[p - 1, ic - 1]
                    cair_bef[p - 1, ic - 1] = cair[p - 1, ic - 1]
                    h2ocan_bef[p - 1, ic - 1] = h2ocan[p - 1, ic - 1]
                    tleaf_bef[p - 1, ic - 1, ISUN - 1] = tleaf[p - 1, ic - 1, ISUN - 1]
                    tleaf_bef[p - 1, ic - 1, ISHA - 1] = tleaf[p - 1, ic - 1, ISHA - 1]
                    lwp_bef[p - 1, ic - 1, ISUN - 1] = lwp[p - 1, ic - 1, ISUN - 1]
                    lwp_bef[p - 1, ic - 1, ISHA - 1] = lwp[p - 1, ic - 1, ISHA - 1]
            mlcanopy_inst = _mlg.getatmforcing(calday_interp_bef, calday_interp_cur, calday_interp_next, calday_interp_ml, num_mlcan, filter_mlcan, mlcanopy_inst)
            mlcanopy_inst = _mls.solarradiation(bounds, num_mlcan, filter_mlcan, mlcanopy_inst)
            mlcanopy_inst = _mlca.canopynitrogenprofile(num_mlcan, filter_mlcan, mlcanopy_inst)
            if (RUNGE_KUTTA_TYPE == I_10):
                nrk_steps = 0
            elif (RUNGE_KUTTA_TYPE == I_20):
                nrk_steps = int((RUNGE_KUTTA_TYPE / I_10))
            for irk in range(1, (nrk_steps + 1) + 1):
                mlcanopy_inst = _mlcano.canopywettedfraction(num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mllo.longwaveradiation(bounds, num_mlcan, filter_mlcan, mlcanopy_inst)
                for fp in range(1, num_mlcan + 1):
                    p = filter_mlcan[fp - 1]
                    for ic in range(1, ncan[p - 1] + 1):
                        rnleaf[p - 1, ic - 1, ISUN - 1] = ((swleaf[p - 1, ic - 1, ISUN - 1, IVIS - 1] + swleaf[p - 1, ic - 1, ISUN - 1, INIR - 1]) + lwleaf[p - 1, ic - 1, ISUN - 1])
                        rnleaf[p - 1, ic - 1, ISHA - 1] = ((swleaf[p - 1, ic - 1, ISHA - 1, IVIS - 1] + swleaf[p - 1, ic - 1, ISHA - 1, INIR - 1]) + lwleaf[p - 1, ic - 1, ISHA - 1])
                    rnsoi[p - 1] = ((swsoi[p - 1, IVIS - 1] + swsoi[p - 1, INIR - 1]) + lwsoi[p - 1])
                mlcanopy_inst = _mlcan.canopyturbulence(nstep_ml, num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mll.leafboundarylayer(num_mlcan, filter_mlcan, ISUN, mlcanopy_inst)
                mlcanopy_inst = _mll.leafboundarylayer(num_mlcan, filter_mlcan, ISHA, mlcanopy_inst)
                mlcanopy_inst = _mllea.leafphotosynthesis(num_mlcan, filter_mlcan, ISUN, mlcanopy_inst)
                mlcanopy_inst = _mllea.leafphotosynthesis(num_mlcan, filter_mlcan, ISHA, mlcanopy_inst)
                mlcanopy_inst = _mlf.fluxprofilesolution(num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mlp.leafwaterpotential(num_mlcan, filter_mlcan, ISUN, mlcanopy_inst)
                mlcanopy_inst = _mlp.leafwaterpotential(num_mlcan, filter_mlcan, ISHA, mlcanopy_inst)
                mlcanopy_inst = _mlcano.canopyinterception(num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mlcano.canopyevaporation(num_mlcan, filter_mlcan, mlcanopy_inst)
                if ((nrk_steps > 0) and (irk <= nrk_steps)):
                    mlcanopy_inst = _mlr.rungekuttaupdate(irk, ark, brk, crk, num_mlcan, filter_mlcan, mlcanopy_inst)
            raise _FGoto('100')  # goto 100
            pass  # write(36,...) log — no dataflow
        except _FGoto as _g:
            if _g.args[0] != '100':
                raise
            pass  # 100 (region exit)
        _out = mltimestepfluxintegration(nstep_ml, num_ml_steps, num_mlcan, filter_mlcan, flux_accumulator, flux_accumulator_profile, flux_accumulator_leaf, mlcanopy_inst)
        _f_copy_out(flux_accumulator, _out[0])
        _f_copy_out(flux_accumulator_profile, _out[1])
        _f_copy_out(flux_accumulator_leaf, _out[2])
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        uref_bef[p - 1] = uref_cur[p - 1]
        tref_bef[p - 1] = tref_cur[p - 1]
        qref_bef[p - 1] = qref_cur[p - 1]
        pref_bef[p - 1] = pref_cur[p - 1]
        co2ref_bef[p - 1] = co2ref_cur[p - 1]
        swskyb_bef[p - 1, IVIS - 1] = swskyb_cur[p - 1, IVIS - 1]
        swskyb_bef[p - 1, INIR - 1] = swskyb_cur[p - 1, INIR - 1]
        swskyd_bef[p - 1, IVIS - 1] = swskyd_cur[p - 1, IVIS - 1]
        swskyd_bef[p - 1, INIR - 1] = swskyd_cur[p - 1, INIR - 1]
        lwsky_bef[p - 1] = lwsky_cur[p - 1]
    mlcanopy_inst = canopyfluxesdiagnostics(num_mlcan, filter_mlcan, mlcanopy_inst)
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            tleaf_hist[p - 1, ic - 1, ISUN - 1] = tleaf[p - 1, ic - 1, ISUN - 1]
            tleaf_hist[p - 1, ic - 1, ISHA - 1] = tleaf[p - 1, ic - 1, ISHA - 1]
            lwp_hist[p - 1, ic - 1, ISUN - 1] = lwp[p - 1, ic - 1, ISUN - 1]
            lwp_hist[p - 1, ic - 1, ISHA - 1] = lwp[p - 1, ic - 1, ISHA - 1]
            if (dpai[p - 1, ic - 1] > 0.0):
                tleaf[p - 1, ic - 1, ISUN - 1] = ((tleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (tleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                tleaf[p - 1, ic - 1, ISHA - 1] = tleaf[p - 1, ic - 1, ISUN - 1]
                lwp[p - 1, ic - 1, ISUN - 1] = ((lwp[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lwp[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lwp[p - 1, ic - 1, ISHA - 1] = lwp[p - 1, ic - 1, ISUN - 1]
    if (MLCAN_TO_CLM == 1):
        for fp in range(1, num_mlcan + 1):
            p = filter_mlcan[fp - 1]
            albd[p - 1, IVIS - 1] = 0.0
            albd[p - 1, INIR - 1] = 0.0
            albi[p - 1, IVIS - 1] = 0.0
            albi[p - 1, INIR - 1] = 0.0
            taux[p - 1] = 0.0
            tauy[p - 1] = 0.0
            eflx_lh_tot[p - 1] = lhflx[p - 1]
            eflx_sh_tot[p - 1] = shflx[p - 1]
            eflx_lwrad_out[p - 1] = lwup[p - 1]
            qflx_evap_tot[p - 1] = (etflx[p - 1] * MMH2O)
            fv[p - 1] = ustar[p - 1]
            u10_clm[p - 1] = 0.0
            t_ref2m[p - 1] = 0.0
            q_ref2m[p - 1] = 0.0
            fsa[p - 1] = (((swveg[p - 1, IVIS - 1] + swveg[p - 1, INIR - 1]) + swsoi[p - 1, IVIS - 1]) + swsoi[p - 1, INIR - 1])
    return canopystate_inst, soilstate_inst, temperature_inst, waterstatebulk_inst, waterfluxbulk_inst, energyflux_inst, frictionvel_inst, surfalb_inst, solarabs_inst, mlcanopy_inst, waterdiagnosticbulk_inst

def getclmvar(nstep, dtime_clm, num_filter, filter, atm2lnd_inst, soilstate_inst, temperature_inst, surfalb_inst, wateratm2lndbulk_inst, mlcanopy_inst):
    """L697-L867 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    c = 0
    g = 0
    lat = 0.0
    lon = 0.0
    coszen = 0.0
    caldaym1 = 0.0
    declinm1 = 0.0
    eccf = 0.0
    # B001 <- L737-L866
    forc_u = atm2lnd_inst.forc_u_grc
    forc_v = atm2lnd_inst.forc_v_grc
    forc_pco2 = atm2lnd_inst.forc_pco2_grc
    forc_po2 = atm2lnd_inst.forc_po2_grc
    forc_solad_col = atm2lnd_inst.forc_solad_downscaled_col
    forc_solai = atm2lnd_inst.forc_solai_grc
    forc_t = atm2lnd_inst.forc_t_downscaled_col
    forc_pbot = atm2lnd_inst.forc_pbot_downscaled_col
    forc_lwrad = atm2lnd_inst.forc_lwrad_downscaled_col
    forc_q = wateratm2lndbulk_inst.forc_q_downscaled_col
    forc_rain = wateratm2lndbulk_inst.forc_rain_downscaled_col
    forc_snow = wateratm2lndbulk_inst.forc_snow_downscaled_col
    albgrd = surfalb_inst.albgrd_col
    albgri = surfalb_inst.albgri_col
    soilresis = soilstate_inst.soilresis_col
    thk = soilstate_inst.thk_col
    t_a10_patch = temperature_inst.t_a10_patch
    t_soisno = temperature_inst.t_soisno_col
    snl = _columntype.col.snl
    z = _columntype.col.z
    zi = _columntype.col.zi
    tref_cur = mlcanopy_inst.tref_cur_forcing
    qref_cur = mlcanopy_inst.qref_cur_forcing
    uref_cur = mlcanopy_inst.uref_cur_forcing
    pref_cur = mlcanopy_inst.pref_cur_forcing
    co2ref_cur = mlcanopy_inst.co2ref_cur_forcing
    o2ref = mlcanopy_inst.o2ref_forcing
    solar_zen = mlcanopy_inst.solar_zen_forcing
    swskyb_cur = mlcanopy_inst.swskyb_cur_forcing
    swskyd_cur = mlcanopy_inst.swskyd_cur_forcing
    lwsky_cur = mlcanopy_inst.lwsky_cur_forcing
    qflx_rain = mlcanopy_inst.qflx_rain_forcing
    qflx_snow = mlcanopy_inst.qflx_snow_forcing
    tacclim = mlcanopy_inst.tacclim_forcing
    albsoib = mlcanopy_inst.albsoib_soil
    albsoid = mlcanopy_inst.albsoid_soil
    soilres = mlcanopy_inst.soilres_soil
    soil_t = mlcanopy_inst.soil_t_soil
    soil_dz = mlcanopy_inst.soil_dz_soil
    soil_tk = mlcanopy_inst.soil_tk_soil
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        c = _patchtype.patch.column[p - 1]
        g = _patchtype.patch.gridcell[p - 1]
        uref_cur[p - 1] = math.sqrt(((forc_u[g - 1] * forc_u[g - 1]) + (forc_v[g - 1] * forc_v[g - 1])))
        swskyd_cur[p - 1, IVIS - 1] = forc_solai[g - 1, IVIS - 1]
        swskyd_cur[p - 1, INIR - 1] = forc_solai[g - 1, INIR - 1]
        tref_cur[p - 1] = forc_t[c - 1]
        qref_cur[p - 1] = forc_q[c - 1]
        pref_cur[p - 1] = forc_pbot[c - 1]
        lwsky_cur[p - 1] = forc_lwrad[c - 1]
        qflx_rain[p - 1] = forc_rain[c - 1]
        qflx_snow[p - 1] = forc_snow[c - 1]
        swskyb_cur[p - 1, IVIS - 1] = forc_solad_col[c - 1, IVIS - 1]
        swskyb_cur[p - 1, INIR - 1] = forc_solad_col[c - 1, INIR - 1]
        co2ref_cur[p - 1] = ((forc_pco2[g - 1] / forc_pbot[c - 1]) * F_1PE06)
        o2ref[p - 1] = ((forc_po2[g - 1] / forc_pbot[c - 1]) * F_1PE03)
        tacclim[p - 1] = t_a10_patch[p - 1]
        albsoib[p - 1, IVIS - 1] = albgrd[c - 1, IVIS - 1]
        albsoib[p - 1, INIR - 1] = albgrd[c - 1, INIR - 1]
        albsoid[p - 1, IVIS - 1] = albgri[c - 1, IVIS - 1]
        albsoid[p - 1, INIR - 1] = albgri[c - 1, INIR - 1]
        soilres[p - 1] = soilresis[c - 1]
        soil_t[p - 1] = t_soisno[c - 1, (snl[c - 1] + 1) - 1]
        soil_dz[p - 1] = ((z[c - 1, (snl[c - 1] + 1) - 1] - zi[c - 1, snl[c - 1] - 1]))
        soil_tk[p - 1] = thk[c - 1, (snl[c - 1] + 1) - 1]
    caldaym1 = _clm.get_curr_calday(offset=(-int(dtime_clm)))
    declinm1, eccf = _shr.shr_orb_decl(caldaym1, _clm_varorb.eccen, _clm_varorb.mvelpp, _clm_varorb.lambm0, _clm_varorb.obliqr)
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        c = _patchtype.patch.column[p - 1]
        g = _patchtype.patch.gridcell[p - 1]
        lat = ((_gri.grc.latdeg[g - 1] * _clm_varcon.rpi) / F_180P)
        lon = ((_gri.grc.londeg[g - 1] * _clm_varcon.rpi) / F_180P)
        coszen = _shr.shr_orb_cosz(caldaym1, lat, lon, declinm1)
        solar_zen[p - 1] = math.acos(_f_max(F_0P01, coszen))
    return mlcanopy_inst

def mltimestepfluxintegration(nstep_ml, num_ml_steps, num_filter, filter, flux_accumulator, flux_accumulator_profile, flux_accumulator_leaf, mlcanopy_inst):
    """L870-L1095 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    i = 0
    j = 0
    k = 0
    # B001 <- L896-L1094
    swskyb = mlcanopy_inst.swskyb_forcing
    swskyd = mlcanopy_inst.swskyd_forcing
    lwsky = mlcanopy_inst.lwsky_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ustar = mlcanopy_inst.ustar_canopy
    beta = mlcanopy_inst.beta_canopy
    obu = mlcanopy_inst.obu_canopy
    z0m = mlcanopy_inst.z0m_canopy
    zdisp = mlcanopy_inst.zdisp_canopy
    lwup = mlcanopy_inst.lwup_canopy
    qflx_intr = mlcanopy_inst.qflx_intr_canopy
    qflx_tflrain = mlcanopy_inst.qflx_tflrain_canopy
    qflx_tflsnow = mlcanopy_inst.qflx_tflsnow_canopy
    swsoi = mlcanopy_inst.swsoi_soil
    lwsoi = mlcanopy_inst.lwsoi_soil
    rnsoi = mlcanopy_inst.rnsoi_soil
    shsoi = mlcanopy_inst.shsoi_soil
    lhsoi = mlcanopy_inst.lhsoi_soil
    etsoi = mlcanopy_inst.etsoi_soil
    gsoi = mlcanopy_inst.gsoi_soil
    gac0 = mlcanopy_inst.gac0_soil
    shair = mlcanopy_inst.shair_profile
    etair = mlcanopy_inst.etair_profile
    stair = mlcanopy_inst.stair_profile
    mflx = mlcanopy_inst.mflx_profile
    kc_eddy = mlcanopy_inst.kc_eddy_profile
    gac = mlcanopy_inst.gac_profile
    swupw = mlcanopy_inst.swupw_profile
    swdwn = mlcanopy_inst.swdwn_profile
    swbeam = mlcanopy_inst.swbeam_profile
    lwupw = mlcanopy_inst.lwupw_profile
    lwdwn = mlcanopy_inst.lwdwn_profile
    swleaf = mlcanopy_inst.swleaf_leaf
    lwleaf = mlcanopy_inst.lwleaf_leaf
    rnleaf = mlcanopy_inst.rnleaf_leaf
    shleaf = mlcanopy_inst.shleaf_leaf
    lhleaf = mlcanopy_inst.lhleaf_leaf
    trleaf = mlcanopy_inst.trleaf_leaf
    evleaf = mlcanopy_inst.evleaf_leaf
    stleaf = mlcanopy_inst.stleaf_leaf
    anet = mlcanopy_inst.anet_leaf
    agross = mlcanopy_inst.agross_leaf
    gs = mlcanopy_inst.gs_leaf
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        if (nstep_ml == 1):
            flux_accumulator[p - 1, :] = 0.0
            flux_accumulator_profile[p - 1, :, :] = 0.0
            flux_accumulator_leaf[p - 1, :, :, :] = 0.0
        i = 0
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + ustar[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + beta[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + obu[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + z0m[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + zdisp[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lwup[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swsoi[p - 1, IVIS - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swsoi[p - 1, INIR - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lwsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + rnsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + shsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lhsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + etsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + gsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + gac0[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + qflx_intr[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + qflx_tflrain[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + qflx_tflsnow[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyb[p - 1, IVIS - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyb[p - 1, INIR - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyd[p - 1, IVIS - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyd[p - 1, INIR - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lwsky[p - 1])
        j = 0
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + shair[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + etair[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + stair[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + mflx[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + kc_eddy[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + gac[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swupw[p - 1, 0 - 1:ncan[p - 1], IVIS - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swupw[p - 1, 0 - 1:ncan[p - 1], INIR - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swdwn[p - 1, 0 - 1:ncan[p - 1], IVIS - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swdwn[p - 1, 0 - 1:ncan[p - 1], INIR - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swbeam[p - 1, 0 - 1:ncan[p - 1], IVIS - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swbeam[p - 1, 0 - 1:ncan[p - 1], INIR - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + lwupw[p - 1, 0 - 1:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + lwdwn[p - 1, 0 - 1:ncan[p - 1]])
        k = 0
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + swleaf[p - 1, :, :, IVIS - 1])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + swleaf[p - 1, :, :, INIR - 1])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + lwleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + rnleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + shleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + lhleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + trleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + evleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + stleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + anet[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + agross[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + gs[p - 1, :, :])
        if (((i > NVAR1D) or (j > NVAR2D)) or (k > NVAR3D)):
            raise RuntimeError('endrun')  # endrun (infra stub)
        if (nstep_ml == num_ml_steps):
            flux_accumulator[p - 1, :] = (flux_accumulator[p - 1, :] / np.float64(num_ml_steps))
            flux_accumulator_profile[p - 1, :, :] = (flux_accumulator_profile[p - 1, :, :] / np.float64(num_ml_steps))
            flux_accumulator_leaf[p - 1, :, :, :] = (flux_accumulator_leaf[p - 1, :, :, :] / np.float64(num_ml_steps))
            i = 0
            i = (i + 1)
            ustar[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            beta[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            obu[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            z0m[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            zdisp[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lwup[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swsoi[p - 1, IVIS - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swsoi[p - 1, INIR - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lwsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            rnsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            shsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lhsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            etsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            gsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            gac0[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            qflx_intr[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            qflx_tflrain[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            qflx_tflsnow[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyb[p - 1, IVIS - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyb[p - 1, INIR - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyd[p - 1, IVIS - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyd[p - 1, INIR - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lwsky[p - 1] = flux_accumulator[p - 1, i - 1]
            j = 0
            j = (j + 1)
            shair[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            etair[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            stair[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            mflx[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            kc_eddy[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            gac[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            swupw[p - 1, 0 - 1:ncan[p - 1], IVIS - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swupw[p - 1, 0 - 1:ncan[p - 1], INIR - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swdwn[p - 1, 0 - 1:ncan[p - 1], IVIS - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swdwn[p - 1, 0 - 1:ncan[p - 1], INIR - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swbeam[p - 1, 0 - 1:ncan[p - 1], IVIS - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swbeam[p - 1, 0 - 1:ncan[p - 1], INIR - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            lwupw[p - 1, 0 - 1:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            lwdwn[p - 1, 0 - 1:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            k = 0
            k = (k + 1)
            swleaf[p - 1, :, :, IVIS - 1] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            swleaf[p - 1, :, :, INIR - 1] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            lwleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            rnleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            shleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            lhleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            trleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            evleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            stleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            anet[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            agross[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            gs[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            if (((i > NVAR1D) or (j > NVAR2D)) or (k > NVAR3D)):
                raise RuntimeError('endrun')  # endrun (infra stub)
    return flux_accumulator, flux_accumulator_profile, flux_accumulator_leaf

def canopyfluxesdiagnostics(num_filter, filter, mlcanopy_inst):
    """L1098-L1511 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    ic = 0
    ib = 0
    err = 0.0
    radin = 0.0
    radout = 0.0
    avail = 0.0
    flux = 0.0
    fracgreen = 0.0
    minlwp = 0.0
    # B001 <- L1130-L1510
    tref = mlcanopy_inst.tref_forcing
    swskyb = mlcanopy_inst.swskyb_forcing
    swskyd = mlcanopy_inst.swskyd_forcing
    lwsky = mlcanopy_inst.lwsky_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    lai = mlcanopy_inst.lai_canopy
    sai = mlcanopy_inst.sai_canopy
    lwup = mlcanopy_inst.lwup_canopy
    shsoi = mlcanopy_inst.shsoi_soil
    lhsoi = mlcanopy_inst.lhsoi_soil
    gsoi = mlcanopy_inst.gsoi_soil
    swsoi = mlcanopy_inst.swsoi_soil
    lwsoi = mlcanopy_inst.lwsoi_soil
    etsoi = mlcanopy_inst.etsoi_soil
    dpai = mlcanopy_inst.dpai_profile
    fwet = mlcanopy_inst.fwet_profile
    fdry = mlcanopy_inst.fdry_profile
    tair = mlcanopy_inst.tair_profile
    wind = mlcanopy_inst.wind_profile
    shair = mlcanopy_inst.shair_profile
    etair = mlcanopy_inst.etair_profile
    stair = mlcanopy_inst.stair_profile
    lwupw = mlcanopy_inst.lwupw_profile
    lwdwn = mlcanopy_inst.lwdwn_profile
    swupw = mlcanopy_inst.swupw_profile
    swdwn = mlcanopy_inst.swdwn_profile
    swbeam = mlcanopy_inst.swbeam_profile
    fracsun = mlcanopy_inst.fracsun_profile
    vcmax25_profile = mlcanopy_inst.vcmax25_profile
    lwleaf = mlcanopy_inst.lwleaf_leaf
    rnleaf = mlcanopy_inst.rnleaf_leaf
    stleaf = mlcanopy_inst.stleaf_leaf
    shleaf = mlcanopy_inst.shleaf_leaf
    lhleaf = mlcanopy_inst.lhleaf_leaf
    trleaf = mlcanopy_inst.trleaf_leaf
    evleaf = mlcanopy_inst.evleaf_leaf
    swleaf = mlcanopy_inst.swleaf_leaf
    agross = mlcanopy_inst.agross_leaf
    apar = mlcanopy_inst.apar_leaf
    anet = mlcanopy_inst.anet_leaf
    gs = mlcanopy_inst.gs_leaf
    tleaf = mlcanopy_inst.tleaf_leaf
    lwp = mlcanopy_inst.lwp_leaf
    vcmax25_leaf = mlcanopy_inst.vcmax25_leaf
    rnet = mlcanopy_inst.rnet_canopy
    stflx_air = mlcanopy_inst.stflx_air_canopy
    stflx_veg = mlcanopy_inst.stflx_veg_canopy
    shflx = mlcanopy_inst.shflx_canopy
    lhflx = mlcanopy_inst.lhflx_canopy
    etflx = mlcanopy_inst.etflx_canopy
    albcan = mlcanopy_inst.albcan_canopy
    swveg = mlcanopy_inst.swveg_canopy
    swvegsun = mlcanopy_inst.swvegsun_canopy
    swvegsha = mlcanopy_inst.swvegsha_canopy
    lwveg = mlcanopy_inst.lwveg_canopy
    lwvegsun = mlcanopy_inst.lwvegsun_canopy
    lwvegsha = mlcanopy_inst.lwvegsha_canopy
    shveg = mlcanopy_inst.shveg_canopy
    shvegsun = mlcanopy_inst.shvegsun_canopy
    shvegsha = mlcanopy_inst.shvegsha_canopy
    lhveg = mlcanopy_inst.lhveg_canopy
    lhvegsun = mlcanopy_inst.lhvegsun_canopy
    lhvegsha = mlcanopy_inst.lhvegsha_canopy
    etveg = mlcanopy_inst.etveg_canopy
    etvegsun = mlcanopy_inst.etvegsun_canopy
    etvegsha = mlcanopy_inst.etvegsha_canopy
    trveg = mlcanopy_inst.trveg_canopy
    evveg = mlcanopy_inst.evveg_canopy
    gppveg = mlcanopy_inst.gppveg_canopy
    gppvegsun = mlcanopy_inst.gppvegsun_canopy
    gppvegsha = mlcanopy_inst.gppvegsha_canopy
    vcmax25veg = mlcanopy_inst.vcmax25veg_canopy
    vcmax25sun = mlcanopy_inst.vcmax25sun_canopy
    vcmax25sha = mlcanopy_inst.vcmax25sha_canopy
    gsveg = mlcanopy_inst.gsveg_canopy
    gsvegsun = mlcanopy_inst.gsvegsun_canopy
    gsvegsha = mlcanopy_inst.gsvegsha_canopy
    windveg = mlcanopy_inst.windveg_canopy
    windvegsun = mlcanopy_inst.windvegsun_canopy
    windvegsha = mlcanopy_inst.windvegsha_canopy
    tlveg = mlcanopy_inst.tlveg_canopy
    tlvegsun = mlcanopy_inst.tlvegsun_canopy
    tlvegsha = mlcanopy_inst.tlvegsha_canopy
    taveg = mlcanopy_inst.taveg_canopy
    tavegsun = mlcanopy_inst.tavegsun_canopy
    tavegsha = mlcanopy_inst.tavegsha_canopy
    laisun = mlcanopy_inst.laisun_canopy
    laisha = mlcanopy_inst.laisha_canopy
    fracminlwp = mlcanopy_inst.fracminlwp_canopy
    swsrc = mlcanopy_inst.swsrc_profile
    lwsrc = mlcanopy_inst.lwsrc_profile
    rnsrc = mlcanopy_inst.rnsrc_profile
    stsrc = mlcanopy_inst.stsrc_profile
    shsrc = mlcanopy_inst.shsrc_profile
    lhsrc = mlcanopy_inst.lhsrc_profile
    etsrc = mlcanopy_inst.etsrc_profile
    trsrc = mlcanopy_inst.trsrc_profile
    evsrc = mlcanopy_inst.evsrc_profile
    fco2src = mlcanopy_inst.fco2src_profile
    swleaf_mean = mlcanopy_inst.swleaf_mean_profile
    lwleaf_mean = mlcanopy_inst.lwleaf_mean_profile
    rnleaf_mean = mlcanopy_inst.rnleaf_mean_profile
    stleaf_mean = mlcanopy_inst.stleaf_mean_profile
    shleaf_mean = mlcanopy_inst.shleaf_mean_profile
    lhleaf_mean = mlcanopy_inst.lhleaf_mean_profile
    etleaf_mean = mlcanopy_inst.etleaf_mean_profile
    trleaf_mean = mlcanopy_inst.trleaf_mean_profile
    evleaf_mean = mlcanopy_inst.evleaf_mean_profile
    fco2_mean = mlcanopy_inst.fco2_mean_profile
    apar_mean = mlcanopy_inst.apar_mean_profile
    gs_mean = mlcanopy_inst.gs_mean_profile
    tleaf_mean = mlcanopy_inst.tleaf_mean_profile
    lwp_mean = mlcanopy_inst.lwp_mean_profile
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                lwleaf_mean[p - 1, ic - 1] = ((lwleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lwleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                swleaf_mean[p - 1, ic - 1, IVIS - 1] = ((swleaf[p - 1, ic - 1, ISUN - 1, IVIS - 1] * fracsun[p - 1, ic - 1]) + (swleaf[p - 1, ic - 1, ISHA - 1, IVIS - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                swleaf_mean[p - 1, ic - 1, INIR - 1] = ((swleaf[p - 1, ic - 1, ISUN - 1, INIR - 1] * fracsun[p - 1, ic - 1]) + (swleaf[p - 1, ic - 1, ISHA - 1, INIR - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                rnleaf_mean[p - 1, ic - 1] = ((rnleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (rnleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                stleaf_mean[p - 1, ic - 1] = ((stleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (stleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                shleaf_mean[p - 1, ic - 1] = ((shleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (shleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lhleaf_mean[p - 1, ic - 1] = ((lhleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lhleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                etleaf_mean[p - 1, ic - 1] = ((((evleaf[p - 1, ic - 1, ISUN - 1] + trleaf[p - 1, ic - 1, ISUN - 1])) * fracsun[p - 1, ic - 1]) + (((evleaf[p - 1, ic - 1, ISHA - 1] + trleaf[p - 1, ic - 1, ISHA - 1])) * ((1.0 - fracsun[p - 1, ic - 1]))))
                trleaf_mean[p - 1, ic - 1] = ((trleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (trleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                evleaf_mean[p - 1, ic - 1] = ((evleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (evleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                fco2_mean[p - 1, ic - 1] = ((anet[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (anet[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                apar_mean[p - 1, ic - 1] = ((apar[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (apar[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                gs_mean[p - 1, ic - 1] = ((gs[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (gs[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                tleaf_mean[p - 1, ic - 1] = ((tleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (tleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lwp_mean[p - 1, ic - 1] = ((lwp[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lwp[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lwsrc[p - 1, ic - 1] = (lwleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                swsrc[p - 1, ic - 1, IVIS - 1] = (swleaf_mean[p - 1, ic - 1, IVIS - 1] * dpai[p - 1, ic - 1])
                swsrc[p - 1, ic - 1, INIR - 1] = (swleaf_mean[p - 1, ic - 1, INIR - 1] * dpai[p - 1, ic - 1])
                rnsrc[p - 1, ic - 1] = (rnleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                stsrc[p - 1, ic - 1] = (stleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                shsrc[p - 1, ic - 1] = (shleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                lhsrc[p - 1, ic - 1] = (lhleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                etsrc[p - 1, ic - 1] = (etleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                trsrc[p - 1, ic - 1] = (trleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                evsrc[p - 1, ic - 1] = (evleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                fracgreen = (fdry[p - 1, ic - 1] / ((1.0 - fwet[p - 1, ic - 1])))
                fco2src[p - 1, ic - 1] = (((((anet[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (anet[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))) * dpai[p - 1, ic - 1]) * fracgreen)
            else:
                lwleaf_mean[p - 1, ic - 1] = 0.0
                swleaf_mean[p - 1, ic - 1, IVIS - 1] = 0.0
                swleaf_mean[p - 1, ic - 1, INIR - 1] = 0.0
                rnleaf_mean[p - 1, ic - 1] = 0.0
                stleaf_mean[p - 1, ic - 1] = 0.0
                shleaf_mean[p - 1, ic - 1] = 0.0
                lhleaf_mean[p - 1, ic - 1] = 0.0
                etleaf_mean[p - 1, ic - 1] = 0.0
                trleaf_mean[p - 1, ic - 1] = 0.0
                evleaf_mean[p - 1, ic - 1] = 0.0
                fco2_mean[p - 1, ic - 1] = 0.0
                apar_mean[p - 1, ic - 1] = 0.0
                gs_mean[p - 1, ic - 1] = 0.0
                tleaf_mean[p - 1, ic - 1] = 0.0
                lwp_mean[p - 1, ic - 1] = 0.0
                lwsrc[p - 1, ic - 1] = 0.0
                swsrc[p - 1, ic - 1, IVIS - 1] = 0.0
                swsrc[p - 1, ic - 1, INIR - 1] = 0.0
                rnsrc[p - 1, ic - 1] = 0.0
                stsrc[p - 1, ic - 1] = 0.0
                shsrc[p - 1, ic - 1] = 0.0
                lhsrc[p - 1, ic - 1] = 0.0
                etsrc[p - 1, ic - 1] = 0.0
                trsrc[p - 1, ic - 1] = 0.0
                evsrc[p - 1, ic - 1] = 0.0
                fco2src[p - 1, ic - 1] = 0.0
        swveg[p - 1, IVIS - 1] = 0.0
        swveg[p - 1, INIR - 1] = 0.0
        lwveg[p - 1] = 0.0
        stflx_veg[p - 1] = 0.0
        shveg[p - 1] = 0.0
        lhveg[p - 1] = 0.0
        etveg[p - 1] = 0.0
        trveg[p - 1] = 0.0
        evveg[p - 1] = 0.0
        gppveg[p - 1] = 0.0
        vcmax25veg[p - 1] = 0.0
        gsveg[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            swveg[p - 1, IVIS - 1] = (swveg[p - 1, IVIS - 1] + swsrc[p - 1, ic - 1, IVIS - 1])
            swveg[p - 1, INIR - 1] = (swveg[p - 1, INIR - 1] + swsrc[p - 1, ic - 1, INIR - 1])
            lwveg[p - 1] = (lwveg[p - 1] + lwsrc[p - 1, ic - 1])
            stflx_veg[p - 1] = (stflx_veg[p - 1] + stsrc[p - 1, ic - 1])
            shveg[p - 1] = (shveg[p - 1] + shsrc[p - 1, ic - 1])
            lhveg[p - 1] = (lhveg[p - 1] + lhsrc[p - 1, ic - 1])
            etveg[p - 1] = (etveg[p - 1] + etsrc[p - 1, ic - 1])
            trveg[p - 1] = (trveg[p - 1] + trsrc[p - 1, ic - 1])
            evveg[p - 1] = (evveg[p - 1] + evsrc[p - 1, ic - 1])
            if (dpai[p - 1, ic - 1] > 0.0):
                fracgreen = (fdry[p - 1, ic - 1] / ((1.0 - fwet[p - 1, ic - 1])))
                gppveg[p - 1] = (gppveg[p - 1] + (((((agross[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (agross[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))) * dpai[p - 1, ic - 1]) * fracgreen))
                gsveg[p - 1] = (gsveg[p - 1] + (gs_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1]))
            vcmax25veg[p - 1] = (vcmax25veg[p - 1] + (vcmax25_profile[p - 1, ic - 1] * dpai[p - 1, ic - 1]))
        err = (((((swveg[p - 1, IVIS - 1] + swveg[p - 1, INIR - 1]) + lwveg[p - 1]) - shveg[p - 1]) - lhveg[p - 1]) - stflx_veg[p - 1])
        if (abs(err) >= F_1PEM03):
            raise RuntimeError('endrun')  # endrun (infra stub)
        for ib in range(1, NUMRAD + 1):
            radin = (swskyb[p - 1, ib - 1] + swskyd[p - 1, ib - 1])
            if (radin > 0.0):
                albcan[p - 1, ib - 1] = (swupw[p - 1, ntop[p - 1] - 1, ib - 1] / radin)
            else:
                albcan[p - 1, ib - 1] = 0.0
        if (FLUX_PROFILE_TYPE == 0) or (FLUX_PROFILE_TYPE == 1):
            shflx[p - 1] = (shveg[p - 1] + shsoi[p - 1])
            etflx[p - 1] = (etveg[p - 1] + etsoi[p - 1])
            lhflx[p - 1] = (lhveg[p - 1] + lhsoi[p - 1])
        elif (FLUX_PROFILE_TYPE == 1):
            shflx[p - 1] = shair[p - 1, ncan[p - 1] - 1]
            etflx[p - 1] = etair[p - 1, ncan[p - 1] - 1]
            lhflx[p - 1] = (etair[p - 1, ncan[p - 1] - 1] * _mlw.latvap(tref[p - 1]))
        else:
            raise RuntimeError('endrun')  # endrun (infra stub)
        stflx_air[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            stflx_air[p - 1] = (stflx_air[p - 1] + stair[p - 1, ic - 1])
        rnet[p - 1] = (((((swveg[p - 1, IVIS - 1] + swveg[p - 1, INIR - 1]) + swsoi[p - 1, IVIS - 1]) + swsoi[p - 1, INIR - 1]) + lwveg[p - 1]) + lwsoi[p - 1])
        radin = ((((swskyb[p - 1, IVIS - 1] + swskyd[p - 1, IVIS - 1]) + swskyb[p - 1, INIR - 1]) + swskyd[p - 1, INIR - 1]) + lwsky[p - 1])
        radout = (((albcan[p - 1, IVIS - 1] * ((swskyb[p - 1, IVIS - 1] + swskyd[p - 1, IVIS - 1]))) + (albcan[p - 1, INIR - 1] * ((swskyb[p - 1, INIR - 1] + swskyd[p - 1, INIR - 1])))) + lwup[p - 1])
        err = (rnet[p - 1] - ((radin - radout)))
        if (abs(err) > F_0P001):
            raise RuntimeError('endrun')  # endrun (infra stub)
        avail = ((radin - radout) - gsoi[p - 1])
        flux = (((shflx[p - 1] + lhflx[p - 1]) + stflx_air[p - 1]) + stflx_veg[p - 1])
        err = (avail - flux)
        if (abs(err) > F_0P01):
            raise RuntimeError('endrun')  # endrun (infra stub)
        ic = int(ntop[p - 1])
        radin = ((((swbeam[p - 1, ic - 1, IVIS - 1] + swbeam[p - 1, ic - 1, INIR - 1]) + swdwn[p - 1, ic - 1, IVIS - 1]) + swdwn[p - 1, ic - 1, INIR - 1]) + lwdwn[p - 1, ic - 1])
        radout = ((swupw[p - 1, ic - 1, IVIS - 1] + swupw[p - 1, ic - 1, INIR - 1]) + lwupw[p - 1, ic - 1])
        err = (((radin - radout)) - rnet[p - 1])
        if (abs(err) > F_0P001):
            raise RuntimeError('endrun')  # endrun (infra stub)
        laisun[p - 1] = 0.0
        laisha[p - 1] = 0.0
        swvegsun[p - 1, 0:NUMRAD] = 0.0
        swvegsha[p - 1, 0:NUMRAD] = 0.0
        lwvegsun[p - 1] = 0.0
        lwvegsha[p - 1] = 0.0
        shvegsun[p - 1] = 0.0
        shvegsha[p - 1] = 0.0
        lhvegsun[p - 1] = 0.0
        lhvegsha[p - 1] = 0.0
        etvegsun[p - 1] = 0.0
        etvegsha[p - 1] = 0.0
        gppvegsun[p - 1] = 0.0
        gppvegsha[p - 1] = 0.0
        vcmax25sun[p - 1] = 0.0
        vcmax25sha[p - 1] = 0.0
        gsvegsun[p - 1] = 0.0
        gsvegsha[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                laisun[p - 1] = (laisun[p - 1] + (fracsun[p - 1, ic - 1] * dpai[p - 1, ic - 1]))
                laisha[p - 1] = (laisha[p - 1] + (((1.0 - fracsun[p - 1, ic - 1])) * dpai[p - 1, ic - 1]))
                swvegsun[p - 1, IVIS - 1] = (swvegsun[p - 1, IVIS - 1] + ((swleaf[p - 1, ic - 1, ISUN - 1, IVIS - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                swvegsun[p - 1, INIR - 1] = (swvegsun[p - 1, INIR - 1] + ((swleaf[p - 1, ic - 1, ISUN - 1, INIR - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                swvegsha[p - 1, IVIS - 1] = (swvegsha[p - 1, IVIS - 1] + ((swleaf[p - 1, ic - 1, ISHA - 1, IVIS - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                swvegsha[p - 1, INIR - 1] = (swvegsha[p - 1, INIR - 1] + ((swleaf[p - 1, ic - 1, ISHA - 1, INIR - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                lwvegsun[p - 1] = (lwvegsun[p - 1] + ((lwleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                lwvegsha[p - 1] = (lwvegsha[p - 1] + ((lwleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                shvegsun[p - 1] = (shvegsun[p - 1] + ((shleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                shvegsha[p - 1] = (shvegsha[p - 1] + ((shleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                lhvegsun[p - 1] = (lhvegsun[p - 1] + ((lhleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                lhvegsha[p - 1] = (lhvegsha[p - 1] + ((lhleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                etvegsun[p - 1] = (etvegsun[p - 1] + ((((evleaf[p - 1, ic - 1, ISUN - 1] + trleaf[p - 1, ic - 1, ISUN - 1])) * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                etvegsha[p - 1] = (etvegsha[p - 1] + ((((evleaf[p - 1, ic - 1, ISHA - 1] + trleaf[p - 1, ic - 1, ISHA - 1])) * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                fracgreen = (fdry[p - 1, ic - 1] / ((1.0 - fwet[p - 1, ic - 1])))
                gppvegsun[p - 1] = (gppvegsun[p - 1] + (((agross[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) * fracgreen))
                gppvegsha[p - 1] = (gppvegsha[p - 1] + (((agross[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) * fracgreen))
                vcmax25sun[p - 1] = (vcmax25sun[p - 1] + ((vcmax25_leaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                vcmax25sha[p - 1] = (vcmax25sha[p - 1] + ((vcmax25_leaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                gsvegsun[p - 1] = (gsvegsun[p - 1] + ((gs[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                gsvegsha[p - 1] = (gsvegsha[p - 1] + ((gs[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
        windveg[p - 1] = 0.0
        windvegsun[p - 1] = 0.0
        windvegsha[p - 1] = 0.0
        tlveg[p - 1] = 0.0
        tlvegsun[p - 1] = 0.0
        tlvegsha[p - 1] = 0.0
        taveg[p - 1] = 0.0
        tavegsun[p - 1] = 0.0
        tavegsha[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                windveg[p - 1] = (windveg[p - 1] + ((wind[p - 1, ic - 1] * dpai[p - 1, ic - 1]) / ((laisun[p - 1] + laisha[p - 1]))))
                windvegsun[p - 1] = (windvegsun[p - 1] + (((wind[p - 1, ic - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) / laisun[p - 1]))
                windvegsha[p - 1] = (windvegsha[p - 1] + (((wind[p - 1, ic - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) / laisha[p - 1]))
                tlveg[p - 1] = (tlveg[p - 1] + ((tleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1]) / ((laisun[p - 1] + laisha[p - 1]))))
                tlvegsun[p - 1] = (tlvegsun[p - 1] + (((tleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) / laisun[p - 1]))
                tlvegsha[p - 1] = (tlvegsha[p - 1] + (((tleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) / laisha[p - 1]))
                taveg[p - 1] = (taveg[p - 1] + ((tair[p - 1, ic - 1] * dpai[p - 1, ic - 1]) / ((laisun[p - 1] + laisha[p - 1]))))
                tavegsun[p - 1] = (tavegsun[p - 1] + (((tair[p - 1, ic - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) / laisun[p - 1]))
                tavegsha[p - 1] = (tavegsha[p - 1] + (((tair[p - 1, ic - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) / laisha[p - 1]))
        minlwp = (-F_2P)
        fracminlwp[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                if (lwp_mean[p - 1, ic - 1] <= minlwp):
                    fracminlwp[p - 1] = (fracminlwp[p - 1] + dpai[p - 1, ic - 1])
        if (((lai[p - 1] + sai[p - 1])) > 0.0):
            fracminlwp[p - 1] = (fracminlwp[p - 1] / ((lai[p - 1] + sai[p - 1])))
    return mlcanopy_inst
