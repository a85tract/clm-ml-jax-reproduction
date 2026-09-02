"""Machine-translated from CLMml_driver.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call clmml_drv before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
from typing import Any

import numpy as np

from clmml_driver_constants import *  # noqa: F401,F403
from clmml_driver_use_constants import *  # noqa: F401,F403
import abortutils_numpy as _abortutils
import atm2lndtype_numpy as _atm
import atm2lndtype_numpy as _atm2lndtype
import canopystatetype_numpy as _can
import canopystatetype_numpy as _canopystatetype
import clm_instmod_numpy as _clm
import clm_instmod_numpy as _clm_instmod
import clm_time_manager_numpy as _clm_
import clm_time_manager_numpy as _clm_time_manager
import clm_varcon_numpy as _clm_varcon
import clm_varctl_numpy as _clm_varctl
import clm_varorb_numpy as _clm_varorb
import clm_varpar_numpy as _clm_varpar
import clmsoiloptionmod_numpy as _clms
import clmsoiloptionmod_numpy as _clmsoiloptionmod
import columntype_numpy as _columntype
import controlmod_numpy as _controlmod
import decompmod_numpy as _decompmod
import energyfluxtype_numpy as _ene
import fileutils_numpy as _fileutils
import filtermod_numpy as _filtermod
import frictionvelocitymod_numpy as _fri
import frictionvelocitymod_numpy as _frictionvelocitymod
import initverticalmod_numpy as _ini
import lnd_comp_nuopc_numpy as _lnd
import lnd_comp_nuopc_numpy as _lnd_comp_nuopc
import mlcanopyfluxestype_numpy as _mlc
import mlcanopyfluxestype_numpy as _mlcanopyfluxestype
import mlclm_varcon_numpy as _mlclm_varcon
import mlclm_varctl_numpy as _mlclm_varctl
import mlclm_varpar_numpy as _mlclm_varpar
import mlwatervapormod_numpy as _mlw
import mlwatervapormod_numpy as _mlwatervapormod
import patchtype_numpy as _patchtype
import shr_kind_mod_numpy as _shr_kind_mod
import shr_orb_mod_numpy as _shr
import shr_orb_mod_numpy as _shr_orb_mod
import soilstateinittimeconstmod_numpy as _soil
import soilstatetype_numpy as _soi
import soilstatetype_numpy as _soilstatetype
import solarabsorbedtype_numpy as _sol
import surfacealbedomod_numpy as _surf
import surfacealbedotype_numpy as _sur
import temperaturetype_numpy as _tem
import temperaturetype_numpy as _temperaturetype
import towerdatamod_numpy as _tow
import towerdatamod_numpy as _towerdatamod
import towermetmod_numpy as _towe
import towermetmod_numpy as _towermetmod
import wateratm2lndbulktype_numpy as _wat
import wateratm2lndbulktype_numpy as _wateratm2lndbulktype
import waterdiagnosticbulktype_numpy as _waterd
import waterfluxbulktype_numpy as _water
import waterstatebulktype_numpy as _wate
import waterstatebulktype_numpy as _waterstatebulktype
import watertype_numpy as _watertype

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'clmml_drv': {'kind': 'subroutine', 'args': [{'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'init_acclim': {'kind': 'subroutine', 'args': [{'name': 'fin', 'dtype': 'str', 'intent': 'IN', 'optional': False}, {'name': 'tower_num', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ntim', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'begp', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'endp', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'atm2lnd_inst', 'dtype': 'UNKNOWN(TYPE(ATM2LND_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'wateratm2lndbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERATM2LNDBULK_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'temperature_inst', 'dtype': 'UNKNOWN(TYPE(TEMPERATURE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'frictionvel_inst', 'dtype': 'UNKNOWN(TYPE(FRICTIONVEL_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'towerveg': {'kind': 'subroutine', 'args': [{'name': 'it', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'begp', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'endp', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'canopystate_inst', 'dtype': 'UNKNOWN(TYPE(CANOPYSTATE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'soilinit': {'kind': 'subroutine', 'args': [{'name': 'ncfilename', 'dtype': 'str', 'intent': 'IN', 'optional': False}, {'name': 'strt', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'begc', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'endc', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'soilstate_inst', 'dtype': 'UNKNOWN(TYPE(SOILSTATE_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'waterstatebulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERSTATEBULK_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'temperature_inst', 'dtype': 'UNKNOWN(TYPE(TEMPERATURE_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'output': {'kind': 'subroutine', 'args': [{'name': 'curr_calday', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'it', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'nout1', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'nout2', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'nout3', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'nout4', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'nout5', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'nout6', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcan', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'temperature_inst', 'dtype': 'UNKNOWN(TYPE(TEMPERATURE_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'readcanopyprofiles': {'kind': 'subroutine', 'args': [{'name': 'itim', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'curr_calday', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'nin1', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}}

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

def _make_clumpfilter():
    """factory for type(clumpfilter) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.num_exposedvegp = 0
    o.exposedvegp = None
    o.num_nolakeurbanp = 0
    o.nolakeurbanp = None
    o.num_nolakec = 0
    o.nolakec = None
    o.num_nourbanc = 0
    o.nourbanc = None
    o.num_hydrologyc = 0
    o.hydrologyc = None
    return o

def _make_patch_type():
    """factory for type(patch_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.column = None
    o.gridcell = None
    o.itype = None
    return o

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

def _make_wateratm2lndbulk_type():
    """factory for type(wateratm2lndbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.forc_q_downscaled_col = None
    o.forc_rain_downscaled_col = None
    o.forc_snow_downscaled_col = None
    return o

def _make_temperature_type():
    """factory for type(temperature_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.t_soisno_col = None
    o.t_a10_patch = None
    o.t_ref2m_patch = None
    return o

def _make_frictionvel_type():
    """factory for type(frictionvel_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.forc_hgt_u_patch = None
    o.u10_clm_patch = None
    o.fv_patch = None
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

def _make_waterstatebulk_type():
    """factory for type(waterstatebulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.h2osoi_liq_col = None
    o.h2osoi_ice_col = None
    o.h2osoi_vol_col = None
    o.h2osfc_col = None
    return o

def _make_water_type():
    """factory for type(water_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.h2osno_col = None
    return o

def _make_waterfluxbulk_type():
    """factory for type(waterfluxbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.qflx_evap_tot_patch = None
    return o

def _make_waterdiagnosticbulk_type():
    """factory for type(waterdiagnosticbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.q_ref2m_patch = None
    o.frac_sno_eff_col = None
    o.bw_col = None
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

def _make_surfalb_type():
    """factory for type(surfalb_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.coszen_col = None
    o.albd_patch = None
    o.albi_patch = None
    o.albgrd_col = None
    o.albgri_col = None
    return o

def _make_solarabs_type():
    """factory for type(solarabs_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.fsa_patch = None
    return o


def clmml_drv(bounds):
    """L32-L295 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    obliq = 0.0
    mvelp = 0.0
    ntim = 0
    itim_next = 0
    time_indx = 0
    curr_time_day = 0
    curr_time_sec = 0
    yr = 0
    mon = 0
    day = 0
    curr_calday = 0.0
    start_calday_clm = 0.0
    run_start_date = 0
    run_start_tod = 0
    clm_start_ymd = 0
    clm_start_tod = 0
    nout1 = 0
    nout2 = 0
    nout3 = 0
    nout4 = 0
    nout5 = 0
    nout6 = 0
    nin1 = 0
    dirout = ''
    ext = ''
    fin_tower = ''
    fin_clm = ''
    fin_soil_adjust = ''
    fout1 = ''
    fout2 = ''
    fout3 = ''
    fout4 = ''
    fout5 = ''
    fout6 = ''
    fin1 = ''
    # B001 <- L89-L89
    ntim, clm_start_ymd, clm_start_tod, fin_tower, fin_clm, fin_soil_adjust, dirout = _controlmod.control()
    # B002 <- L96-L96
    _clm_.itim = 1
    # B003 <- L97-L97
    yr, mon, day, _clm_.curr_date_tod = _clm_.get_curr_date()
    # B004 <- L99-L99
    pass  # write(iulog,...) log — no dataflow
    # B005 <- L110-L110
    _lnd.initializerealize(bounds)
    # B006 <- L114-L114
    _filtermod.filter = _filtermod.setfilters(_filtermod.filter)
    # B007 <- L120-L120
    _clm_varorb.eccen, obliq, mvelp, _clm_varorb.obliqr, _clm_varorb.lambm0, _clm_varorb.mvelpp = _shr.shr_orb_params(yr)
    # B008 <- L126-L127
    _clm.atm2lnd_inst, _clm.wateratm2lndbulk_inst, _clm.temperature_inst, _clm.frictionvel_inst, _clm.mlcanopy_inst = init_acclim(fin_tower, _tow.tower_num, ntim, bounds.begp, bounds.endp, _clm.atm2lnd_inst, _clm.wateratm2lndbulk_inst, _clm.temperature_inst, _clm.frictionvel_inst, _clm.mlcanopy_inst)
    # B009 <- L133-L133
    _clm.canopystate_inst, _clm.mlcanopy_inst = towerveg(_tow.tower_num, bounds.begp, bounds.endp, _clm.canopystate_inst, _clm.mlcanopy_inst)
    # B010 <- L145-L145
    run_start_date = _clm_.start_date_ymd
    # B011 <- L146-L146
    run_start_tod = _clm_.start_date_tod
    # B012 <- L148-L148
    _clm_.start_date_ymd = clm_start_ymd
    # B013 <- L149-L149
    _clm_.start_date_tod = clm_start_tod
    # B014 <- L151-L151
    _clm_.itim = 1
    # B015 <- L152-L152
    start_calday_clm = _clm_.get_curr_calday(offset=0)
    # B016 <- L156-L156
    _clm_.start_date_ymd = run_start_date
    # B017 <- L157-L157
    _clm_.start_date_tod = run_start_tod
    # B018 <- L159-L159
    _clm_.itim = 1
    # B019 <- L160-L160
    curr_calday = _clm_.get_curr_calday(offset=0)
    # B020 <- L164-L164
    time_indx = (_f_nint(((((curr_calday - start_calday_clm)) * F_86400P) / np.float64(_clm_.dtstep))) + 1)
    # B021 <- L168-L169
    _clm.waterstatebulk_inst, _clm.temperature_inst = soilinit(fin_clm, time_indx, bounds.begc, bounds.endc, _clm.soilstate_inst, _clm.waterstatebulk_inst, _clm.temperature_inst)
    # B022 <- L178-L178 AGENT_QUEUE: formatted internal write
    raise NotImplementedError('formatted internal write')  # B022
    # B023 <- L179-L179
    fout1 = (dirout[0:len(_f_trim(dirout))] + ext[0:len(_f_trim(ext))])
    # B024 <- L180-L180
    nout1 = 6
    # B025 <- L181-L181
    pass  # OPEN/CLOSE (I/O stub)
    # B026 <- L183-L183 AGENT_QUEUE: formatted internal write
    raise NotImplementedError('formatted internal write')  # B026
    # B027 <- L184-L184
    fout2 = (dirout[0:len(_f_trim(dirout))] + ext[0:len(_f_trim(ext))])
    # B028 <- L185-L185
    nout2 = 6
    # B029 <- L186-L186
    pass  # OPEN/CLOSE (I/O stub)
    # B030 <- L188-L188 AGENT_QUEUE: formatted internal write
    raise NotImplementedError('formatted internal write')  # B030
    # B031 <- L189-L189
    fout3 = (dirout[0:len(_f_trim(dirout))] + ext[0:len(_f_trim(ext))])
    # B032 <- L190-L190
    nout3 = 6
    # B033 <- L191-L191
    pass  # OPEN/CLOSE (I/O stub)
    # B034 <- L193-L193 AGENT_QUEUE: formatted internal write
    raise NotImplementedError('formatted internal write')  # B034
    # B035 <- L194-L194
    fout4 = (dirout[0:len(_f_trim(dirout))] + ext[0:len(_f_trim(ext))])
    # B036 <- L195-L195
    nout4 = 6
    # B037 <- L196-L196
    pass  # OPEN/CLOSE (I/O stub)
    # B038 <- L198-L198 AGENT_QUEUE: formatted internal write
    raise NotImplementedError('formatted internal write')  # B038
    # B039 <- L199-L199
    fout5 = (dirout[0:len(_f_trim(dirout))] + ext[0:len(_f_trim(ext))])
    # B040 <- L200-L200
    nout5 = 6
    # B041 <- L201-L201
    pass  # OPEN/CLOSE (I/O stub)
    # B042 <- L203-L203 AGENT_QUEUE: formatted internal write
    raise NotImplementedError('formatted internal write')  # B042
    # B043 <- L204-L204
    fout6 = (dirout[0:len(_f_trim(dirout))] + ext[0:len(_f_trim(ext))])
    # B044 <- L205-L205
    nout6 = 6
    # B045 <- L206-L206
    pass  # OPEN/CLOSE (I/O stub)
    # B046 <- L212-L218 AGENT_QUEUE: formatted internal write
    raise NotImplementedError('formatted internal write')  # B046
    # B047 <- L224-L224
    pass  # write(iulog,...) log — no dataflow
    # B048 <- L226-L269
    for itim in range(1, ntim + 1):
        yr, mon, day, _clm_.curr_date_tod = _clm_.get_curr_date()
        curr_time_day, curr_time_sec = _clm_.get_curr_time()
        curr_calday = _clm_.get_curr_calday(offset=0)
        time_indx = (_f_nint(((((curr_calday - start_calday_clm)) * F_86400P) / np.float64(_clm_.dtstep))) + 1)
        _clm.atm2lnd_inst, _clm.wateratm2lndbulk_inst, _clm.frictionvel_inst = _towe.towermetcurr(fin_tower, _clm_.itim, _tow.tower_num, bounds.begp, bounds.endp)
        if (MET_TYPE == I_3):
            itim_next = _f_min((_clm_.itim + 1), ntim)
            _towe.towermetnext(fin_tower, itim_next, bounds.begp, bounds.endp, _clm.mlcanopy_inst)
        if (FLUX_PROFILE_TYPE == (-1)):
            _clm.mlcanopy_inst = readcanopyprofiles(_clm_.itim, curr_calday, nin1, _clm.mlcanopy_inst)
        _lnd.modeladvance(bounds, time_indx, fin_clm, fin_soil_adjust)
        if (_clm_.itim == 1):
            pass  # write(iulog,...) log — no dataflow
        output(curr_calday, _tow.tower_num, nout1, nout2, nout3, nout4, nout5, nout6, _clm.mlcanopy_inst, _clm.temperature_inst)
    # B049 <- L275-L275
    pass  # OPEN/CLOSE (I/O stub)
    # B050 <- L276-L276
    pass  # relavu (infra stub)
    # B051 <- L277-L277
    pass  # OPEN/CLOSE (I/O stub)
    # B052 <- L278-L278
    pass  # relavu (infra stub)
    # B053 <- L279-L279
    pass  # OPEN/CLOSE (I/O stub)
    # B054 <- L280-L280
    pass  # relavu (infra stub)
    # B055 <- L281-L281
    pass  # OPEN/CLOSE (I/O stub)
    # B056 <- L282-L282
    pass  # relavu (infra stub)
    # B057 <- L283-L283
    pass  # OPEN/CLOSE (I/O stub)
    # B058 <- L284-L284
    pass  # relavu (infra stub)
    # B059 <- L285-L285
    pass  # OPEN/CLOSE (I/O stub)
    # B060 <- L286-L286
    pass  # relavu (infra stub)
    # B061 <- L288-L291
    if (FLUX_PROFILE_TYPE == (-1)):
        pass  # OPEN/CLOSE (I/O stub)
        pass  # relavu (infra stub)
    # B062 <- L293-L293
    pass  # write(iulog,...) log — no dataflow
    return

def init_acclim(fin, tower_num, ntim, begp, endp, atm2lnd_inst, wateratm2lndbulk_inst, temperature_inst, frictionvel_inst, mlcanopy_inst):
    """L298-L374 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    p = 0
    c = 0
    itim = 0
    # B001 <- L331-L373
    forc_t = atm2lnd_inst.forc_t_downscaled_col
    forc_pbot = atm2lnd_inst.forc_pbot_downscaled_col
    t10 = temperature_inst.t_a10_patch
    pref = mlcanopy_inst.pref_forcing
    for p in range(begp, endp + 1):
        t10[p - 1] = 0.0
    for itim in range(1, ntim + 1):
        atm2lnd_inst, wateratm2lndbulk_inst, frictionvel_inst = _towe.towermetcurr(fin, itim, tower_num, begp, endp)
        for p in range(begp, endp + 1):
            c = _patchtype.patch.column[p - 1]
            t10[p - 1] = (t10[p - 1] + forc_t[c - 1])
            if (itim == 1):
                pref[p - 1] = forc_pbot[c - 1]
    for p in range(begp, endp + 1):
        t10[p - 1] = (t10[p - 1] / np.float64(ntim))
    return atm2lnd_inst, wateratm2lndbulk_inst, temperature_inst, frictionvel_inst, mlcanopy_inst

def towerveg(it, begp, endp, canopystate_inst, mlcanopy_inst):
    """L377-L450 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    p = 0
    htop_pft = np.empty(((MXPFT) - (0) + 1,), dtype=np.float64)
    htop_pft[0 - 1] = 0.0
    htop_pft[1:17] = np.array([F_17P, F_17P, F_14P, F_35P, F_35P, F_18P, F_20P, F_20P, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], dtype=np.float64)
    pass  # DATA DATA non-literal bound mxpft (AGENT_QUEUE)
    # B001 <- L408-L449
    htop = canopystate_inst.htop_patch
    root_biomass = mlcanopy_inst.root_biomass_canopy
    pbeta_lai = mlcanopy_inst.pbeta_lai_canopy
    pbeta_sai = mlcanopy_inst.pbeta_sai_canopy
    for p in range(begp, endp + 1):
        _patchtype.patch.itype[p - 1] = _tow.tower_pft[it - 1]
        if (_tow.tower_canht[it - 1] > 0.0):
            htop[p - 1] = _tow.tower_canht[it - 1]
        else:
            htop[p - 1] = htop_pft[(_patchtype.patch.itype[p - 1]) - (0)]
        if (_tow.tower_root[it - 1] > 0.0):
            root_biomass[p - 1] = _tow.tower_root[it - 1]
        else:
            raise RuntimeError('endrun')  # endrun (infra stub)
        if ((((_tow.tower_pbeta_lai[it - 1, 0] > 0.0) and (_tow.tower_pbeta_lai[it - 1, 1] > 0.0)) and (_tow.tower_pbeta_sai[it - 1, 0] > 0.0)) and (_tow.tower_pbeta_sai[it - 1, 1] > 0.0)):
            pbeta_lai[p - 1, 0] = _tow.tower_pbeta_lai[it - 1, 0]
            pbeta_lai[p - 1, 1] = _tow.tower_pbeta_lai[it - 1, 1]
            pbeta_sai[p - 1, 0] = _tow.tower_pbeta_sai[it - 1, 0]
            pbeta_sai[p - 1, 1] = _tow.tower_pbeta_sai[it - 1, 1]
    return canopystate_inst, mlcanopy_inst

def soilinit(ncfilename, strt, begc, endc, soilstate_inst, waterstatebulk_inst, temperature_inst):
    """L453-L583 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    c = 0
    j = 0
    ncid = 0
    status = 0
    varid = 0
    start3 = np.empty((I_3,), dtype=np.int32)
    count3 = np.empty((I_3,), dtype=np.int32)
    tsoi_loc = np.empty((1, 1, NLEVGRND,), dtype=np.float64)
    h2osoi_loc_clm45 = np.empty((1, 1, NLEVGRND,), dtype=np.float64)
    h2osoi_loc_clm50 = np.empty((1, 1, NLEVSOI,), dtype=np.float64)
    # B001 <- L492-L582
    dz = _columntype.col.dz
    nbedrock = _columntype.col.nbedrock
    watsat = soilstate_inst.watsat_col
    t_soisno = temperature_inst.t_soisno_col
    h2osoi_vol = waterstatebulk_inst.h2osoi_vol_col
    h2osoi_ice = waterstatebulk_inst.h2osoi_ice_col
    h2osoi_liq = waterstatebulk_inst.h2osoi_liq_col
    status = int(nf_open[ncfilename - 1, nf_nowrite - 1, ncid - 1])
    if (status != nf_noerr):
        raise RuntimeError('endrun')  # handle_err (infra stub)
    start3[...] = np.array([1, 1, strt])
    status = int(nf_inq_varid(ncid, 'TSOI', varid))
    if (status != nf_noerr):
        raise RuntimeError('endrun')  # handle_err (infra stub)
    count3[...] = np.array([1, NLEVGRND, 1])
    status = int(nf_get_vara_double[ncid - 1, varid - 1, ((start3) - 1), ((count3) - 1), ((tsoi_loc) - 1)])
    if (status != nf_noerr):
        raise RuntimeError('endrun')  # handle_err (infra stub)
    status = int(nf_inq_varid(ncid, 'H2OSOI', varid))
    if (status != nf_noerr):
        raise RuntimeError('endrun')  # handle_err (infra stub)
    if (_fstr_eq(_clms.clm_phys, 'CLM4_5')):
        count3[...] = np.array([1, NLEVGRND, 1])
        status = int(nf_get_vara_double[ncid - 1, varid - 1, ((start3) - 1), ((count3) - 1), ((h2osoi_loc_clm45) - 1)])
        if (status != nf_noerr):
            raise RuntimeError('endrun')  # handle_err (infra stub)
    elif (_fstr_eq(_clms.clm_phys, 'CLM5_0')):
        count3[...] = np.array([1, NLEVSOI, 1])
        status = int(nf_get_vara_double[ncid - 1, varid - 1, ((start3) - 1), ((count3) - 1), ((h2osoi_loc_clm50) - 1)])
        if (status != nf_noerr):
            raise RuntimeError('endrun')  # handle_err (infra stub)
    status = int(nf_close[ncid - 1])
    for c in range(begc, endc + 1):
        for j in range(1, NLEVGRND + 1):
            t_soisno[c - 1, j - 1] = tsoi_loc[0, 0, j - 1]
        if (_fstr_eq(_clms.clm_phys, 'CLM4_5')):
            for j in range(1, NLEVGRND + 1):
                h2osoi_vol[c - 1, j - 1] = h2osoi_loc_clm45[0, 0, j - 1]
        elif (_fstr_eq(_clms.clm_phys, 'CLM5_0')):
            for j in range(1, NLEVSOI + 1):
                h2osoi_vol[c - 1, j - 1] = h2osoi_loc_clm50[0, 0, j - 1]
            for j in range((NLEVSOI + 1), NLEVGRND + 1):
                h2osoi_vol[c - 1, j - 1] = 0.0
        if (_fstr_eq(_clms.clm_phys, 'CLM5_0')):
            for j in range(1, nbedrock[c - 1] + 1):
                h2osoi_vol[c - 1, j - 1] = _f_min(h2osoi_vol[c - 1, j - 1], watsat[c - 1, j - 1])
        for j in range(1, NLEVGRND + 1):
            h2osoi_liq[c - 1, j - 1] = ((h2osoi_vol[c - 1, j - 1] * dz[c - 1, j - 1]) * DENH2O)
            h2osoi_ice[c - 1, j - 1] = 0.0
    return waterstatebulk_inst, temperature_inst

def output(curr_calday, it, nout1, nout2, nout3, nout4, nout5, nout6, mlcan, temperature_inst):
    """L586-L805 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    ic = 0
    top = 0
    mid = 0
    p = 0
    swup = 0.0
    tair = 0.0
    qair = 0.0
    eair = 0.0
    ra = 0.0
    lad = 0.0
    missing_value = 0.0
    zero_value = 0.0
    shf = 0.0
    lhf = 0.0
    mflx = 0.0
    lhflx_tr = 0.0
    lhflx_ev = 0.0
    time_stamp = 0.0
    # B001 <- L637-L637
    missing_value = (-F_999P)
    # B002 <- L638-L638
    zero_value = 0.0
    # B003 <- L640-L640
    p = 1
    # B004 <- L644-L655
    if (MET_TYPE == 0):
        time_stamp = curr_calday
    elif (MET_TYPE == I_3):
        time_stamp = (curr_calday - ((0.5 * _clm_.dtstep) / F_86400P))
    elif (MET_TYPE == 2):
        time_stamp = curr_calday
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B005 <- L661-L662
    swup = ((mlcan.albcan_canopy[p - 1, IVIS - 1] * ((mlcan.swskyb_forcing[p - 1, IVIS - 1] + mlcan.swskyd_forcing[p - 1, IVIS - 1]))) + (mlcan.albcan_canopy[p - 1, INIR - 1] * ((mlcan.swskyb_forcing[p - 1, INIR - 1] + mlcan.swskyd_forcing[p - 1, INIR - 1]))))
    # B006 <- L668-L668
    lhflx_tr = (mlcan.trveg_canopy[p - 1] * _mlw.latvap(mlcan.tref_forcing[p - 1]))
    # B007 <- L669-L669
    lhflx_ev = (mlcan.evveg_canopy[p - 1] * _mlw.latvap(mlcan.tref_forcing[p - 1]))
    # B008 <- L670-L670
    ic = mlcan.ntop_canopy[p - 1]
    # B009 <- L671-L671
    tair = mlcan.tair_profile[p - 1, ic - 1]
    # B010 <- L673-L676
    pass  # write(nout1,...) log — no dataflow
    # B011 <- L682-L693
    pass  # write(nout4,...) log — no dataflow
    # B012 <- L699-L699
    top = mlcan.ntop_canopy[p - 1]
    # B013 <- L700-L700
    mid = _f_max(1, ((mlcan.nbot_canopy[p - 1] + _f_int_div((((mlcan.ntop_canopy[p - 1] - mlcan.nbot_canopy[p - 1]) + 1)), 2)) - 1))
    # B014 <- L702-L703
    pass  # write(nout2,...) log — no dataflow
    # B015 <- L711-L731
    for ic in range(mlcan.ncan_canopy[p - 1], (mlcan.ntop_canopy[p - 1] + 1) - 1, (-1)):
        tair = mlcan.tair_profile[p - 1, ic - 1]
        qair = (((F_1000P * ((MMH2O / MMDRY))) * mlcan.eair_profile[p - 1, ic - 1]) / ((mlcan.pref_forcing[p - 1] - (((1.0 - (MMH2O / MMDRY))) * mlcan.eair_profile[p - 1, ic - 1]))))
        eair = (mlcan.eair_profile[p - 1, ic - 1] / F_1000P)
        ra = (mlcan.rhomol_forcing[p - 1] / mlcan.gac_profile[p - 1, ic - 1])
        lad = (mlcan.dpai_profile[p - 1, ic - 1] / mlcan.dz_profile[p - 1, ic - 1])
        pass  # write(nout3,...) log — no dataflow
    # B016 <- L735-L773
    for ic in range(mlcan.ntop_canopy[p - 1], 1 - 1, (-1)):
        tair = mlcan.tair_profile[p - 1, ic - 1]
        qair = (((F_1000P * ((MMH2O / MMDRY))) * mlcan.eair_profile[p - 1, ic - 1]) / ((mlcan.pref_forcing[p - 1] - (((1.0 - (MMH2O / MMDRY))) * mlcan.eair_profile[p - 1, ic - 1]))))
        eair = (mlcan.eair_profile[p - 1, ic - 1] / F_1000P)
        ra = (mlcan.rhomol_forcing[p - 1] / mlcan.gac_profile[p - 1, ic - 1])
        lad = (mlcan.dpai_profile[p - 1, ic - 1] / mlcan.dz_profile[p - 1, ic - 1])
        if (mlcan.dpai_profile[p - 1, ic - 1] > 0.0):
            pass  # write(nout3,...) log — no dataflow
        else:
            pass  # write(nout3,...) log — no dataflow
    # B017 <- L780-L796
    for ic in range(mlcan.ncan_canopy[p - 1], 1 - 1, (-1)):
        shf = mlcan.shair_profile[p - 1, ic - 1]
        lhf = (mlcan.etair_profile[p - 1, ic - 1] * _mlw.latvap(mlcan.tref_forcing[p - 1]))
        mflx = mlcan.mflx_profile[p - 1, ic - 1]
        pass  # write(nout5,...) log — no dataflow
    # B018 <- L802-L803
    pass  # write(nout6,...) log — no dataflow
    return

def readcanopyprofiles(itim, curr_calday, nin1, mlcanopy_inst):
    """L808-L898 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    p = 0
    ic = 0
    err = 0.0
    curr_calday_data = 0.0
    zs_data = 0.0
    wind = 0.0
    tair = 0.0
    qair = 0.0
    x = np.empty((I_22,), dtype=np.float64)
    i = 0
    nrec = 0
    check = 0.0
    # B001 <- L839-L897
    ncan = mlcanopy_inst.ncan_canopy
    pref = mlcanopy_inst.pref_forcing
    zs = mlcanopy_inst.zs_profile
    wind_data = mlcanopy_inst.wind_data_profile
    tair_data = mlcanopy_inst.tair_data_profile
    eair_data = mlcanopy_inst.eair_data_profile
    p = 1
    if (itim == 1):
        nrec = 0
        while True:
            pass  # READ (I/O stub)
            if (nrec == 0):
                check = curr_calday_data
            if (curr_calday_data == check):
                nrec = (nrec + 1)
            else:
                break
        ncan[p - 1] = nrec
        pass  # REWIND (I/O stub)
    for ic in range(ncan[p - 1], 1 - 1, (-1)):
        pass  # READ (I/O stub)
        qair = (qair / F_1000P)
        err = (curr_calday_data - curr_calday)
        if (abs(err) >= F_1PEM04):
            raise RuntimeError('endrun')  # endrun (infra stub)
        if (itim > 1):
            err = (zs_data - zs[p - 1, ic - 1])
            if (abs(err) >= F_1PEM03):
                raise RuntimeError('endrun')  # endrun (infra stub)
        wind_data[p - 1, ic - 1] = wind
        tair_data[p - 1, ic - 1] = tair
        eair_data[p - 1, ic - 1] = ((qair * pref[p - 1]) / (((MMH2O / MMDRY) + (((1.0 - (MMH2O / MMDRY))) * qair))))
    return mlcanopy_inst


# Flattened adapters for the differential gate (recast-clm, flatten.py).
class _Record:
    def __init__(self, **fields):
        self.__dict__.update(fields)

def clmml_drv_flat(np_, bounds__begc, bounds__begp, bounds__endc, bounds__endp):
    bounds = _Record(begc=bounds__begc, begp=bounds__begp, endc=bounds__endc, endp=bounds__endp)
    _out = clmml_drv(bounds=bounds)
    return None

_SIGNATURES.update({
    'clmml_drv_flat': {'kind': 'subroutine', 'args': [{'name': 'np_', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'bounds__begc', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}, {'name': 'bounds__begp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}, {'name': 'bounds__endc', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}, {'name': 'bounds__endp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}], 'result': None, 'result_dtype': None},
})
