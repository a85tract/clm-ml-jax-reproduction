"""Machine-translated from MLCanopyFluxesType.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call init before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
from typing import Any

import numpy as np

from mlcanopyfluxestype_constants import *  # noqa: F401,F403
from mlcanopyfluxestype_use_constants import *  # noqa: F401,F403
import abortutils_numpy as _abortutils
import clm_varcon_numpy as _clm_varcon
import clm_varpar_numpy as _clm_varpar
import decompmod_numpy as _decompmod
import histfilemod_numpy as _histfilemod
import mlclm_varctl_numpy as _mlc
import mlclm_varctl_numpy as _mlclm_varctl
import mlclm_varpar_numpy as _mlclm_varpar
import ncdio_pio_numpy as _ncdio_pio
import restutilmod_numpy as _restutilmod
import shr_kind_mod_numpy as _shr_kind_mod

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'init': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(MLCANOPY_TYPE))', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'initallocate': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(MLCANOPY_TYPE))', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'inithistory': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(MLCANOPY_TYPE))', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'initcold': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(MLCANOPY_TYPE))', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'restart': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(MLCANOPY_TYPE))', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'ncid', 'dtype': 'UNKNOWN(TYPE(FILE_DESC_T))', 'intent': 'INOUT', 'optional': False}, {'name': 'flag', 'dtype': 'str', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}}

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


def init(this, bounds):
    """L368-L382 subroutine (machine-translated)."""
    # B001 <- L378-L378 AGENT_QUEUE: call to external subroutine 'this % initallocate'
    raise NotImplementedError("call to external subroutine 'this % initallocate'")  # B001
    # B002 <- L379-L379 AGENT_QUEUE: call to external subroutine 'this % inithistory'
    raise NotImplementedError("call to external subroutine 'this % inithistory'")  # B002
    # B003 <- L380-L380 AGENT_QUEUE: call to external subroutine 'this % initcold'
    raise NotImplementedError("call to external subroutine 'this % initcold'")  # B003
    return

def initallocate(this, bounds):
    """L385-L705 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    begp = 0
    endp = 0
    # B001 <- L399-L399
    begp = int(bounds.begp)
    # B002 <- L399-L399
    endp = int(bounds.endp)
    # B003 <- L403-L403
    this.ztop_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B004 <- L403-L403
    this.ztop_canopy[:] = _clm_varcon.spval
    # B005 <- L404-L404
    this.zbot_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B006 <- L404-L404
    this.zbot_canopy[:] = _clm_varcon.spval
    # B007 <- L405-L405
    this.lai_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B008 <- L405-L405
    this.lai_canopy[:] = _clm_varcon.spval
    # B009 <- L406-L406
    this.sai_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B010 <- L406-L406
    this.sai_canopy[:] = _clm_varcon.spval
    # B011 <- L407-L407
    this.root_biomass_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B012 <- L407-L407
    this.root_biomass_canopy[:] = _clm_varcon.spval
    # B013 <- L408-L408
    this.pbeta_lai_canopy = np.empty(((endp) - (begp) + 1, 2), dtype=np.float64)
    # B014 <- L408-L408
    this.pbeta_lai_canopy[:, :] = (-_clm_varcon.spval)
    # B015 <- L409-L409
    this.pbeta_sai_canopy = np.empty(((endp) - (begp) + 1, 2), dtype=np.float64)
    # B016 <- L409-L409
    this.pbeta_sai_canopy[:, :] = (-_clm_varcon.spval)
    # B017 <- L413-L413
    this.zref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B018 <- L413-L413
    this.zref_forcing[:] = _clm_varcon.spval
    # B019 <- L414-L414
    this.tref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B020 <- L414-L414
    this.tref_forcing[:] = _clm_varcon.spval
    # B021 <- L415-L415
    this.tref_bef_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B022 <- L415-L415
    this.tref_bef_forcing[:] = _clm_varcon.spval
    # B023 <- L416-L416
    this.tref_cur_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B024 <- L416-L416
    this.tref_cur_forcing[:] = _clm_varcon.spval
    # B025 <- L417-L417
    this.tref_next_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B026 <- L417-L417
    this.tref_next_forcing[:] = _clm_varcon.spval
    # B027 <- L418-L418
    this.qref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B028 <- L418-L418
    this.qref_forcing[:] = _clm_varcon.spval
    # B029 <- L419-L419
    this.qref_bef_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B030 <- L419-L419
    this.qref_bef_forcing[:] = _clm_varcon.spval
    # B031 <- L420-L420
    this.qref_cur_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B032 <- L420-L420
    this.qref_cur_forcing[:] = _clm_varcon.spval
    # B033 <- L421-L421
    this.qref_next_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B034 <- L421-L421
    this.qref_next_forcing[:] = _clm_varcon.spval
    # B035 <- L422-L422
    this.uref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B036 <- L422-L422
    this.uref_forcing[:] = _clm_varcon.spval
    # B037 <- L423-L423
    this.uref_bef_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B038 <- L423-L423
    this.uref_bef_forcing[:] = _clm_varcon.spval
    # B039 <- L424-L424
    this.uref_cur_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B040 <- L424-L424
    this.uref_cur_forcing[:] = _clm_varcon.spval
    # B041 <- L425-L425
    this.uref_next_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B042 <- L425-L425
    this.uref_next_forcing[:] = _clm_varcon.spval
    # B043 <- L426-L426
    this.pref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B044 <- L426-L426
    this.pref_forcing[:] = _clm_varcon.spval
    # B045 <- L427-L427
    this.pref_bef_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B046 <- L427-L427
    this.pref_bef_forcing[:] = _clm_varcon.spval
    # B047 <- L428-L428
    this.pref_cur_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B048 <- L428-L428
    this.pref_cur_forcing[:] = _clm_varcon.spval
    # B049 <- L429-L429
    this.pref_next_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B050 <- L429-L429
    this.pref_next_forcing[:] = _clm_varcon.spval
    # B051 <- L430-L430
    this.co2ref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B052 <- L430-L430
    this.co2ref_forcing[:] = _clm_varcon.spval
    # B053 <- L431-L431
    this.co2ref_bef_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B054 <- L431-L431
    this.co2ref_bef_forcing[:] = _clm_varcon.spval
    # B055 <- L432-L432
    this.co2ref_cur_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B056 <- L432-L432
    this.co2ref_cur_forcing[:] = _clm_varcon.spval
    # B057 <- L433-L433
    this.co2ref_next_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B058 <- L433-L433
    this.co2ref_next_forcing[:] = _clm_varcon.spval
    # B059 <- L434-L434
    this.o2ref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B060 <- L434-L434
    this.o2ref_forcing[:] = _clm_varcon.spval
    # B061 <- L435-L435
    this.swskyb_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B062 <- L435-L435
    this.swskyb_forcing[:, :] = _clm_varcon.spval
    # B063 <- L436-L436
    this.swskyb_bef_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B064 <- L436-L436
    this.swskyb_bef_forcing[:, :] = _clm_varcon.spval
    # B065 <- L437-L437
    this.swskyb_cur_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B066 <- L437-L437
    this.swskyb_cur_forcing[:, :] = _clm_varcon.spval
    # B067 <- L438-L438
    this.swskyb_next_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B068 <- L438-L438
    this.swskyb_next_forcing[:, :] = _clm_varcon.spval
    # B069 <- L439-L439
    this.swskyd_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B070 <- L439-L439
    this.swskyd_forcing[:, :] = _clm_varcon.spval
    # B071 <- L440-L440
    this.swskyd_bef_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B072 <- L440-L440
    this.swskyd_bef_forcing[:, :] = _clm_varcon.spval
    # B073 <- L441-L441
    this.swskyd_cur_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B074 <- L441-L441
    this.swskyd_cur_forcing[:, :] = _clm_varcon.spval
    # B075 <- L442-L442
    this.swskyd_next_forcing = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B076 <- L442-L442
    this.swskyd_next_forcing[:, :] = _clm_varcon.spval
    # B077 <- L443-L443
    this.lwsky_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B078 <- L443-L443
    this.lwsky_forcing[:] = _clm_varcon.spval
    # B079 <- L444-L444
    this.lwsky_bef_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B080 <- L444-L444
    this.lwsky_bef_forcing[:] = _clm_varcon.spval
    # B081 <- L445-L445
    this.lwsky_cur_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B082 <- L445-L445
    this.lwsky_cur_forcing[:] = _clm_varcon.spval
    # B083 <- L446-L446
    this.lwsky_next_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B084 <- L446-L446
    this.lwsky_next_forcing[:] = _clm_varcon.spval
    # B085 <- L447-L447
    this.qflx_rain_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B086 <- L447-L447
    this.qflx_rain_forcing[:] = _clm_varcon.spval
    # B087 <- L448-L448
    this.qflx_snow_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B088 <- L448-L448
    this.qflx_snow_forcing[:] = _clm_varcon.spval
    # B089 <- L449-L449
    this.tacclim_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B090 <- L449-L449
    this.tacclim_forcing[:] = _clm_varcon.spval
    # B091 <- L453-L453
    this.eref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B092 <- L453-L453
    this.eref_forcing[:] = _clm_varcon.spval
    # B093 <- L454-L454
    this.thref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B094 <- L454-L454
    this.thref_forcing[:] = _clm_varcon.spval
    # B095 <- L455-L455
    this.thvref_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B096 <- L455-L455
    this.thvref_forcing[:] = _clm_varcon.spval
    # B097 <- L456-L456
    this.rhoair_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B098 <- L456-L456
    this.rhoair_forcing[:] = _clm_varcon.spval
    # B099 <- L457-L457
    this.rhomol_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B100 <- L457-L457
    this.rhomol_forcing[:] = _clm_varcon.spval
    # B101 <- L458-L458
    this.mmair_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B102 <- L458-L458
    this.mmair_forcing[:] = _clm_varcon.spval
    # B103 <- L459-L459
    this.cpair_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B104 <- L459-L459
    this.cpair_forcing[:] = _clm_varcon.spval
    # B105 <- L460-L460
    this.solar_zen_forcing = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B106 <- L460-L460
    this.solar_zen_forcing[:] = _clm_varcon.spval
    # B107 <- L464-L464
    this.swveg_canopy = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B108 <- L464-L464
    this.swveg_canopy[:, :] = _clm_varcon.spval
    # B109 <- L465-L465
    this.swvegsun_canopy = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B110 <- L465-L465
    this.swvegsun_canopy[:, :] = _clm_varcon.spval
    # B111 <- L466-L466
    this.swvegsha_canopy = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B112 <- L466-L466
    this.swvegsha_canopy[:, :] = _clm_varcon.spval
    # B113 <- L467-L467
    this.lwveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B114 <- L467-L467
    this.lwveg_canopy[:] = _clm_varcon.spval
    # B115 <- L468-L468
    this.lwvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B116 <- L468-L468
    this.lwvegsun_canopy[:] = _clm_varcon.spval
    # B117 <- L469-L469
    this.lwvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B118 <- L469-L469
    this.lwvegsha_canopy[:] = _clm_varcon.spval
    # B119 <- L470-L470
    this.shveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B120 <- L470-L470
    this.shveg_canopy[:] = _clm_varcon.spval
    # B121 <- L471-L471
    this.shvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B122 <- L471-L471
    this.shvegsun_canopy[:] = _clm_varcon.spval
    # B123 <- L472-L472
    this.shvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B124 <- L472-L472
    this.shvegsha_canopy[:] = _clm_varcon.spval
    # B125 <- L473-L473
    this.lhveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B126 <- L473-L473
    this.lhveg_canopy[:] = _clm_varcon.spval
    # B127 <- L474-L474
    this.lhvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B128 <- L474-L474
    this.lhvegsun_canopy[:] = _clm_varcon.spval
    # B129 <- L475-L475
    this.lhvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B130 <- L475-L475
    this.lhvegsha_canopy[:] = _clm_varcon.spval
    # B131 <- L476-L476
    this.etveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B132 <- L476-L476
    this.etveg_canopy[:] = _clm_varcon.spval
    # B133 <- L477-L477
    this.etvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B134 <- L477-L477
    this.etvegsun_canopy[:] = _clm_varcon.spval
    # B135 <- L478-L478
    this.etvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B136 <- L478-L478
    this.etvegsha_canopy[:] = _clm_varcon.spval
    # B137 <- L479-L479
    this.trveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B138 <- L479-L479
    this.trveg_canopy[:] = _clm_varcon.spval
    # B139 <- L480-L480
    this.evveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B140 <- L480-L480
    this.evveg_canopy[:] = _clm_varcon.spval
    # B141 <- L481-L481
    this.gppveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B142 <- L481-L481
    this.gppveg_canopy[:] = _clm_varcon.spval
    # B143 <- L482-L482
    this.gppvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B144 <- L482-L482
    this.gppvegsun_canopy[:] = _clm_varcon.spval
    # B145 <- L483-L483
    this.gppvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B146 <- L483-L483
    this.gppvegsha_canopy[:] = _clm_varcon.spval
    # B147 <- L484-L484
    this.vcmax25veg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B148 <- L484-L484
    this.vcmax25veg_canopy[:] = _clm_varcon.spval
    # B149 <- L485-L485
    this.vcmax25sun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B150 <- L485-L485
    this.vcmax25sun_canopy[:] = _clm_varcon.spval
    # B151 <- L486-L486
    this.vcmax25sha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B152 <- L486-L486
    this.vcmax25sha_canopy[:] = _clm_varcon.spval
    # B153 <- L487-L487
    this.gsveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B154 <- L487-L487
    this.gsveg_canopy[:] = _clm_varcon.spval
    # B155 <- L488-L488
    this.gsvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B156 <- L488-L488
    this.gsvegsun_canopy[:] = _clm_varcon.spval
    # B157 <- L489-L489
    this.gsvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B158 <- L489-L489
    this.gsvegsha_canopy[:] = _clm_varcon.spval
    # B159 <- L490-L490
    this.windveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B160 <- L490-L490
    this.windveg_canopy[:] = _clm_varcon.spval
    # B161 <- L491-L491
    this.windvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B162 <- L491-L491
    this.windvegsun_canopy[:] = _clm_varcon.spval
    # B163 <- L492-L492
    this.windvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B164 <- L492-L492
    this.windvegsha_canopy[:] = _clm_varcon.spval
    # B165 <- L493-L493
    this.tlveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B166 <- L493-L493
    this.tlveg_canopy[:] = _clm_varcon.spval
    # B167 <- L494-L494
    this.tlvegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B168 <- L494-L494
    this.tlvegsun_canopy[:] = _clm_varcon.spval
    # B169 <- L495-L495
    this.tlvegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B170 <- L495-L495
    this.tlvegsha_canopy[:] = _clm_varcon.spval
    # B171 <- L496-L496
    this.taveg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B172 <- L496-L496
    this.taveg_canopy[:] = _clm_varcon.spval
    # B173 <- L497-L497
    this.tavegsun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B174 <- L497-L497
    this.tavegsun_canopy[:] = _clm_varcon.spval
    # B175 <- L498-L498
    this.tavegsha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B176 <- L498-L498
    this.tavegsha_canopy[:] = _clm_varcon.spval
    # B177 <- L499-L499
    this.laisun_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B178 <- L499-L499
    this.laisun_canopy[:] = _clm_varcon.spval
    # B179 <- L500-L500
    this.laisha_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B180 <- L500-L500
    this.laisha_canopy[:] = _clm_varcon.spval
    # B181 <- L501-L501
    this.albcan_canopy = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B182 <- L501-L501
    this.albcan_canopy[:, :] = _clm_varcon.spval
    # B183 <- L502-L502
    this.lwup_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B184 <- L502-L502
    this.lwup_canopy[:] = _clm_varcon.spval
    # B185 <- L503-L503
    this.rnet_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B186 <- L503-L503
    this.rnet_canopy[:] = _clm_varcon.spval
    # B187 <- L504-L504
    this.shflx_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B188 <- L504-L504
    this.shflx_canopy[:] = _clm_varcon.spval
    # B189 <- L505-L505
    this.lhflx_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B190 <- L505-L505
    this.lhflx_canopy[:] = _clm_varcon.spval
    # B191 <- L506-L506
    this.etflx_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B192 <- L506-L506
    this.etflx_canopy[:] = _clm_varcon.spval
    # B193 <- L507-L507
    this.stflx_air_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B194 <- L507-L507
    this.stflx_air_canopy[:] = _clm_varcon.spval
    # B195 <- L508-L508
    this.stflx_veg_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B196 <- L508-L508
    this.stflx_veg_canopy[:] = _clm_varcon.spval
    # B197 <- L509-L509
    this.ustar_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B198 <- L509-L509
    this.ustar_canopy[:] = _clm_varcon.spval
    # B199 <- L510-L510
    this.gac_to_hc_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B200 <- L510-L510
    this.gac_to_hc_canopy[:] = _clm_varcon.spval
    # B201 <- L511-L511
    this.qflx_intr_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B202 <- L511-L511
    this.qflx_intr_canopy[:] = _clm_varcon.spval
    # B203 <- L512-L512
    this.qflx_tflrain_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B204 <- L512-L512
    this.qflx_tflrain_canopy[:] = _clm_varcon.spval
    # B205 <- L513-L513
    this.qflx_tflsnow_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B206 <- L513-L513
    this.qflx_tflsnow_canopy[:] = _clm_varcon.spval
    # B207 <- L517-L517
    this.uaf_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B208 <- L517-L517
    this.uaf_canopy[:] = _clm_varcon.spval
    # B209 <- L518-L518
    this.taf_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B210 <- L518-L518
    this.taf_canopy[:] = _clm_varcon.spval
    # B211 <- L519-L519
    this.qaf_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B212 <- L519-L519
    this.qaf_canopy[:] = _clm_varcon.spval
    # B213 <- L520-L520
    this.fracminlwp_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B214 <- L520-L520
    this.fracminlwp_canopy[:] = _clm_varcon.spval
    # B215 <- L524-L524
    this.obu_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B216 <- L524-L524
    this.obu_canopy[:] = _clm_varcon.spval
    # B217 <- L525-L525
    this.beta_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B218 <- L525-L525
    this.beta_canopy[:] = _clm_varcon.spval
    # B219 <- L526-L526
    this.prsc_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B220 <- L526-L526
    this.prsc_canopy[:] = _clm_varcon.spval
    # B221 <- L527-L527
    this.lc_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B222 <- L527-L527
    this.lc_canopy[:] = _clm_varcon.spval
    # B223 <- L528-L528
    this.zdisp_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B224 <- L528-L528
    this.zdisp_canopy[:] = _clm_varcon.spval
    # B225 <- L529-L529
    this.z0m_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B226 <- L529-L529
    this.z0m_canopy[:] = _clm_varcon.spval
    # B227 <- L533-L533
    this.g0_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B228 <- L533-L533
    this.g0_canopy[:] = _clm_varcon.spval
    # B229 <- L534-L534
    this.g1_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B230 <- L534-L534
    this.g1_canopy[:] = _clm_varcon.spval
    # B231 <- L538-L538
    this.albsoib_soil = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B232 <- L538-L538
    this.albsoib_soil[:, :] = _clm_varcon.spval
    # B233 <- L539-L539
    this.albsoid_soil = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B234 <- L539-L539
    this.albsoid_soil[:, :] = _clm_varcon.spval
    # B235 <- L540-L540
    this.swsoi_soil = np.empty(((endp) - (begp) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B236 <- L540-L540
    this.swsoi_soil[:, :] = _clm_varcon.spval
    # B237 <- L541-L541
    this.lwsoi_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B238 <- L541-L541
    this.lwsoi_soil[:] = _clm_varcon.spval
    # B239 <- L542-L542
    this.rnsoi_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B240 <- L542-L542
    this.rnsoi_soil[:] = _clm_varcon.spval
    # B241 <- L543-L543
    this.shsoi_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B242 <- L543-L543
    this.shsoi_soil[:] = _clm_varcon.spval
    # B243 <- L544-L544
    this.lhsoi_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B244 <- L544-L544
    this.lhsoi_soil[:] = _clm_varcon.spval
    # B245 <- L545-L545
    this.etsoi_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B246 <- L545-L545
    this.etsoi_soil[:] = _clm_varcon.spval
    # B247 <- L546-L546
    this.gsoi_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B248 <- L546-L546
    this.gsoi_soil[:] = _clm_varcon.spval
    # B249 <- L547-L547
    this.tg_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B250 <- L547-L547
    this.tg_soil[:] = _clm_varcon.spval
    # B251 <- L548-L548
    this.tg_bef_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B252 <- L548-L548
    this.tg_bef_soil[:] = _clm_varcon.spval
    # B253 <- L549-L549
    this.dtg_soil = np.empty(((endp) - (begp) + 1, _mlc.NRK), dtype=np.float64)
    # B254 <- L549-L549
    this.dtg_soil[:, :] = _clm_varcon.spval
    # B255 <- L550-L550
    this.eg_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B256 <- L550-L550
    this.eg_soil[:] = _clm_varcon.spval
    # B257 <- L551-L551
    this.rhg_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B258 <- L551-L551
    this.rhg_soil[:] = _clm_varcon.spval
    # B259 <- L552-L552
    this.gac0_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B260 <- L552-L552
    this.gac0_soil[:] = _clm_varcon.spval
    # B261 <- L553-L553
    this.soil_t_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B262 <- L553-L553
    this.soil_t_soil[:] = _clm_varcon.spval
    # B263 <- L554-L554
    this.soil_dz_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B264 <- L554-L554
    this.soil_dz_soil[:] = _clm_varcon.spval
    # B265 <- L555-L555
    this.soil_tk_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B266 <- L555-L555
    this.soil_tk_soil[:] = _clm_varcon.spval
    # B267 <- L556-L556
    this.soilres_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B268 <- L556-L556
    this.soilres_soil[:] = _clm_varcon.spval
    # B269 <- L560-L560
    this.btran_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B270 <- L560-L560
    this.btran_soil[:] = _clm_varcon.spval
    # B271 <- L561-L561
    this.psis_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B272 <- L561-L561
    this.psis_soil[:] = _clm_varcon.spval
    # B273 <- L562-L562
    this.rsoil_soil = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B274 <- L562-L562
    this.rsoil_soil[:] = _clm_varcon.spval
    # B275 <- L563-L563
    this.soil_et_loss_soil = np.empty(((endp) - (begp) + 1, _clm_varpar.nlevgrnd), dtype=np.float64)
    # B276 <- L563-L563
    this.soil_et_loss_soil[:, :] = _clm_varcon.spval
    # B277 <- L567-L567
    this.ncan_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B278 <- L567-L567
    this.ncan_canopy[:] = _clm_varcon.ispval
    # B279 <- L568-L568
    this.ntop_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B280 <- L568-L568
    this.ntop_canopy[:] = _clm_varcon.ispval
    # B281 <- L569-L569
    this.nbot_canopy = np.empty(((endp) - (begp) + 1,), dtype=np.float64)
    # B282 <- L569-L569
    this.nbot_canopy[:] = _clm_varcon.ispval
    # B283 <- L573-L573
    this.dlai_frac_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B284 <- L573-L573
    this.dlai_frac_profile[:, :] = _clm_varcon.spval
    # B285 <- L574-L574
    this.dsai_frac_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B286 <- L574-L574
    this.dsai_frac_profile[:, :] = _clm_varcon.spval
    # B287 <- L575-L575
    this.dlai_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B288 <- L575-L575
    this.dlai_profile[:, :] = _clm_varcon.spval
    # B289 <- L576-L576
    this.dsai_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B290 <- L576-L576
    this.dsai_profile[:, :] = _clm_varcon.spval
    # B291 <- L577-L577
    this.dpai_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B292 <- L577-L577
    this.dpai_profile[:, :] = _clm_varcon.spval
    # B293 <- L578-L578
    this.zs_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B294 <- L578-L578
    this.zs_profile[:, :] = _clm_varcon.spval
    # B295 <- L579-L579
    this.zw_profile = np.empty(((endp) - (begp) + 1, (NLEVMLCAN) - (0) + 1), dtype=np.float64)
    # B296 <- L579-L579
    this.zw_profile[:, :] = _clm_varcon.spval
    # B297 <- L580-L580
    this.dz_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B298 <- L580-L580
    this.dz_profile[:, :] = _clm_varcon.spval
    # B299 <- L582-L582
    this.vcmax25_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B300 <- L582-L582
    this.vcmax25_profile[:, :] = _clm_varcon.spval
    # B301 <- L583-L583
    this.jmax25_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B302 <- L583-L583
    this.jmax25_profile[:, :] = _clm_varcon.spval
    # B303 <- L584-L584
    this.kp25_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B304 <- L584-L584
    this.kp25_profile[:, :] = _clm_varcon.spval
    # B305 <- L585-L585
    this.rd25_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B306 <- L585-L585
    this.rd25_profile[:, :] = _clm_varcon.spval
    # B307 <- L586-L586
    this.cpleaf_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B308 <- L586-L586
    this.cpleaf_profile[:, :] = _clm_varcon.spval
    # B309 <- L588-L588
    this.fracsun_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B310 <- L588-L588
    this.fracsun_profile[:, :] = _clm_varcon.spval
    # B311 <- L589-L589
    this.kb_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B312 <- L589-L589
    this.kb_profile[:, :] = _clm_varcon.spval
    # B313 <- L590-L590
    this.tb_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B314 <- L590-L590
    this.tb_profile[:, :] = _clm_varcon.spval
    # B315 <- L591-L591
    this.td_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B316 <- L591-L591
    this.td_profile[:, :] = _clm_varcon.spval
    # B317 <- L592-L592
    this.tbi_profile = np.empty(((endp) - (begp) + 1, (NLEVMLCAN) - (0) + 1), dtype=np.float64)
    # B318 <- L592-L592
    this.tbi_profile[:, :] = _clm_varcon.spval
    # B319 <- L593-L593
    this.swbeam_profile = np.empty(((endp) - (begp) + 1, (NLEVMLCAN) - (0) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B320 <- L593-L593
    this.swbeam_profile[:, :, :] = _clm_varcon.spval
    # B321 <- L594-L594
    this.swupw_profile = np.empty(((endp) - (begp) + 1, (NLEVMLCAN) - (0) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B322 <- L594-L594
    this.swupw_profile[:, :, :] = _clm_varcon.spval
    # B323 <- L595-L595
    this.swdwn_profile = np.empty(((endp) - (begp) + 1, (NLEVMLCAN) - (0) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B324 <- L595-L595
    this.swdwn_profile[:, :, :] = _clm_varcon.spval
    # B325 <- L596-L596
    this.lwupw_profile = np.empty(((endp) - (begp) + 1, (NLEVMLCAN) - (0) + 1), dtype=np.float64)
    # B326 <- L596-L596
    this.lwupw_profile[:, :] = _clm_varcon.spval
    # B327 <- L597-L597
    this.lwdwn_profile = np.empty(((endp) - (begp) + 1, (NLEVMLCAN) - (0) + 1), dtype=np.float64)
    # B328 <- L597-L597
    this.lwdwn_profile[:, :] = _clm_varcon.spval
    # B329 <- L599-L599
    this.swsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN, _clm_varpar.NUMRAD), dtype=np.float64)
    # B330 <- L599-L599
    this.swsrc_profile[:, :, :] = _clm_varcon.spval
    # B331 <- L600-L600
    this.lwsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B332 <- L600-L600
    this.lwsrc_profile[:, :] = _clm_varcon.spval
    # B333 <- L601-L601
    this.rnsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B334 <- L601-L601
    this.rnsrc_profile[:, :] = _clm_varcon.spval
    # B335 <- L602-L602
    this.stsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B336 <- L602-L602
    this.stsrc_profile[:, :] = _clm_varcon.spval
    # B337 <- L603-L603
    this.shsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B338 <- L603-L603
    this.shsrc_profile[:, :] = _clm_varcon.spval
    # B339 <- L604-L604
    this.lhsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B340 <- L604-L604
    this.lhsrc_profile[:, :] = _clm_varcon.spval
    # B341 <- L605-L605
    this.etsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B342 <- L605-L605
    this.etsrc_profile[:, :] = _clm_varcon.spval
    # B343 <- L606-L606
    this.trsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B344 <- L606-L606
    this.trsrc_profile[:, :] = _clm_varcon.spval
    # B345 <- L607-L607
    this.evsrc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B346 <- L607-L607
    this.evsrc_profile[:, :] = _clm_varcon.spval
    # B347 <- L608-L608
    this.fco2src_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B348 <- L608-L608
    this.fco2src_profile[:, :] = _clm_varcon.spval
    # B349 <- L610-L610
    this.wind_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B350 <- L610-L610
    this.wind_profile[:, :] = _clm_varcon.spval
    # B351 <- L611-L611
    this.tair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B352 <- L611-L611
    this.tair_profile[:, :] = _clm_varcon.spval
    # B353 <- L612-L612
    this.eair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B354 <- L612-L612
    this.eair_profile[:, :] = _clm_varcon.spval
    # B355 <- L613-L613
    this.cair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B356 <- L613-L613
    this.cair_profile[:, :] = _clm_varcon.spval
    # B357 <- L614-L614
    this.tair_bef_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B358 <- L614-L614
    this.tair_bef_profile[:, :] = _clm_varcon.spval
    # B359 <- L615-L615
    this.eair_bef_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B360 <- L615-L615
    this.eair_bef_profile[:, :] = _clm_varcon.spval
    # B361 <- L616-L616
    this.cair_bef_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B362 <- L616-L616
    this.cair_bef_profile[:, :] = _clm_varcon.spval
    # B363 <- L617-L617
    this.dtair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN, _mlc.NRK), dtype=np.float64)
    # B364 <- L617-L617
    this.dtair_profile[:, :, :] = _clm_varcon.spval
    # B365 <- L618-L618
    this.deair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN, _mlc.NRK), dtype=np.float64)
    # B366 <- L618-L618
    this.deair_profile[:, :, :] = _clm_varcon.spval
    # B367 <- L619-L619
    this.wind_data_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B368 <- L619-L619
    this.wind_data_profile[:, :] = _clm_varcon.spval
    # B369 <- L620-L620
    this.tair_data_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B370 <- L620-L620
    this.tair_data_profile[:, :] = _clm_varcon.spval
    # B371 <- L621-L621
    this.eair_data_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B372 <- L621-L621
    this.eair_data_profile[:, :] = _clm_varcon.spval
    # B373 <- L623-L623
    this.shair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B374 <- L623-L623
    this.shair_profile[:, :] = _clm_varcon.spval
    # B375 <- L624-L624
    this.etair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B376 <- L624-L624
    this.etair_profile[:, :] = _clm_varcon.spval
    # B377 <- L625-L625
    this.stair_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B378 <- L625-L625
    this.stair_profile[:, :] = _clm_varcon.spval
    # B379 <- L626-L626
    this.mflx_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B380 <- L626-L626
    this.mflx_profile[:, :] = _clm_varcon.spval
    # B381 <- L627-L627
    this.gac_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B382 <- L627-L627
    this.gac_profile[:, :] = _clm_varcon.spval
    # B383 <- L628-L628
    this.kc_eddy_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B384 <- L628-L628
    this.kc_eddy_profile[:, :] = _clm_varcon.spval
    # B385 <- L630-L630
    this.swleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN, _clm_varpar.NUMRAD), dtype=np.float64)
    # B386 <- L630-L630
    this.swleaf_mean_profile[:, :, :] = _clm_varcon.spval
    # B387 <- L631-L631
    this.lwleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B388 <- L631-L631
    this.lwleaf_mean_profile[:, :] = _clm_varcon.spval
    # B389 <- L632-L632
    this.rnleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B390 <- L632-L632
    this.rnleaf_mean_profile[:, :] = _clm_varcon.spval
    # B391 <- L633-L633
    this.stleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B392 <- L633-L633
    this.stleaf_mean_profile[:, :] = _clm_varcon.spval
    # B393 <- L634-L634
    this.shleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B394 <- L634-L634
    this.shleaf_mean_profile[:, :] = _clm_varcon.spval
    # B395 <- L635-L635
    this.lhleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B396 <- L635-L635
    this.lhleaf_mean_profile[:, :] = _clm_varcon.spval
    # B397 <- L636-L636
    this.etleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B398 <- L636-L636
    this.etleaf_mean_profile[:, :] = _clm_varcon.spval
    # B399 <- L637-L637
    this.trleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B400 <- L637-L637
    this.trleaf_mean_profile[:, :] = _clm_varcon.spval
    # B401 <- L638-L638
    this.evleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B402 <- L638-L638
    this.evleaf_mean_profile[:, :] = _clm_varcon.spval
    # B403 <- L639-L639
    this.fco2_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B404 <- L639-L639
    this.fco2_mean_profile[:, :] = _clm_varcon.spval
    # B405 <- L640-L640
    this.apar_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B406 <- L640-L640
    this.apar_mean_profile[:, :] = _clm_varcon.spval
    # B407 <- L641-L641
    this.gs_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B408 <- L641-L641
    this.gs_mean_profile[:, :] = _clm_varcon.spval
    # B409 <- L642-L642
    this.tleaf_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B410 <- L642-L642
    this.tleaf_mean_profile[:, :] = _clm_varcon.spval
    # B411 <- L643-L643
    this.lwp_mean_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B412 <- L643-L643
    this.lwp_mean_profile[:, :] = _clm_varcon.spval
    # B413 <- L645-L645
    this.lsc_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B414 <- L645-L645
    this.lsc_profile[:, :] = _clm_varcon.spval
    # B415 <- L646-L646
    this.h2ocan_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B416 <- L646-L646
    this.h2ocan_profile[:, :] = _clm_varcon.spval
    # B417 <- L647-L647
    this.h2ocan_bef_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B418 <- L647-L647
    this.h2ocan_bef_profile[:, :] = _clm_varcon.spval
    # B419 <- L648-L648
    this.dh2ocan_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN, _mlc.NRK), dtype=np.float64)
    # B420 <- L648-L648
    this.dh2ocan_profile[:, :, :] = _clm_varcon.spval
    # B421 <- L649-L649
    this.fwet_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B422 <- L649-L649
    this.fwet_profile[:, :] = _clm_varcon.spval
    # B423 <- L650-L650
    this.fdry_profile = np.empty(((endp) - (begp) + 1, NLEVMLCAN), dtype=np.float64)
    # B424 <- L650-L650
    this.fdry_profile[:, :] = _clm_varcon.spval
    # B425 <- L654-L654
    this.tleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B426 <- L654-L654
    this.tleaf_leaf[:, :, :] = _clm_varcon.spval
    # B427 <- L655-L655
    this.tleaf_bef_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B428 <- L655-L655
    this.tleaf_bef_leaf[:, :, :] = _clm_varcon.spval
    # B429 <- L656-L656
    this.dtleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF, _mlc.NRK), dtype=np.float64)
    # B430 <- L656-L656
    this.dtleaf_leaf[:, :, :, :] = _clm_varcon.spval
    # B431 <- L657-L657
    this.tleaf_hist_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B432 <- L657-L657
    this.tleaf_hist_leaf[:, :, :] = _clm_varcon.spval
    # B433 <- L658-L658
    this.swleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF, _clm_varpar.NUMRAD), dtype=np.float64)
    # B434 <- L658-L658
    this.swleaf_leaf[:, :, :, :] = _clm_varcon.spval
    # B435 <- L659-L659
    this.lwleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B436 <- L659-L659
    this.lwleaf_leaf[:, :, :] = _clm_varcon.spval
    # B437 <- L660-L660
    this.rnleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B438 <- L660-L660
    this.rnleaf_leaf[:, :, :] = _clm_varcon.spval
    # B439 <- L661-L661
    this.stleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B440 <- L661-L661
    this.stleaf_leaf[:, :, :] = _clm_varcon.spval
    # B441 <- L662-L662
    this.shleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B442 <- L662-L662
    this.shleaf_leaf[:, :, :] = _clm_varcon.spval
    # B443 <- L663-L663
    this.lhleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B444 <- L663-L663
    this.lhleaf_leaf[:, :, :] = _clm_varcon.spval
    # B445 <- L664-L664
    this.trleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B446 <- L664-L664
    this.trleaf_leaf[:, :, :] = _clm_varcon.spval
    # B447 <- L665-L665
    this.evleaf_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B448 <- L665-L665
    this.evleaf_leaf[:, :, :] = _clm_varcon.spval
    # B449 <- L667-L667
    this.gbh_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B450 <- L667-L667
    this.gbh_leaf[:, :, :] = _clm_varcon.spval
    # B451 <- L668-L668
    this.gbv_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B452 <- L668-L668
    this.gbv_leaf[:, :, :] = _clm_varcon.spval
    # B453 <- L669-L669
    this.gbc_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B454 <- L669-L669
    this.gbc_leaf[:, :, :] = _clm_varcon.spval
    # B455 <- L671-L671
    this.vcmax25_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B456 <- L671-L671
    this.vcmax25_leaf[:, :, :] = _clm_varcon.spval
    # B457 <- L672-L672
    this.jmax25_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B458 <- L672-L672
    this.jmax25_leaf[:, :, :] = _clm_varcon.spval
    # B459 <- L673-L673
    this.kp25_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B460 <- L673-L673
    this.kp25_leaf[:, :, :] = _clm_varcon.spval
    # B461 <- L674-L674
    this.rd25_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B462 <- L674-L674
    this.rd25_leaf[:, :, :] = _clm_varcon.spval
    # B463 <- L676-L676
    this.kc_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B464 <- L676-L676
    this.kc_leaf[:, :, :] = _clm_varcon.spval
    # B465 <- L677-L677
    this.ko_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B466 <- L677-L677
    this.ko_leaf[:, :, :] = _clm_varcon.spval
    # B467 <- L678-L678
    this.cp_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B468 <- L678-L678
    this.cp_leaf[:, :, :] = _clm_varcon.spval
    # B469 <- L679-L679
    this.vcmax_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B470 <- L679-L679
    this.vcmax_leaf[:, :, :] = _clm_varcon.spval
    # B471 <- L680-L680
    this.jmax_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B472 <- L680-L680
    this.jmax_leaf[:, :, :] = _clm_varcon.spval
    # B473 <- L681-L681
    this.kp_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B474 <- L681-L681
    this.kp_leaf[:, :, :] = _clm_varcon.spval
    # B475 <- L682-L682
    this.ceair_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B476 <- L682-L682
    this.ceair_leaf[:, :, :] = _clm_varcon.spval
    # B477 <- L683-L683
    this.leaf_esat_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B478 <- L683-L683
    this.leaf_esat_leaf[:, :, :] = _clm_varcon.spval
    # B479 <- L685-L685
    this.apar_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B480 <- L685-L685
    this.apar_leaf[:, :, :] = _clm_varcon.spval
    # B481 <- L686-L686
    this.je_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B482 <- L686-L686
    this.je_leaf[:, :, :] = _clm_varcon.spval
    # B483 <- L687-L687
    this.ac_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B484 <- L687-L687
    this.ac_leaf[:, :, :] = _clm_varcon.spval
    # B485 <- L688-L688
    this.aj_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B486 <- L688-L688
    this.aj_leaf[:, :, :] = _clm_varcon.spval
    # B487 <- L689-L689
    this.ap_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B488 <- L689-L689
    this.ap_leaf[:, :, :] = _clm_varcon.spval
    # B489 <- L690-L690
    this.agross_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B490 <- L690-L690
    this.agross_leaf[:, :, :] = _clm_varcon.spval
    # B491 <- L691-L691
    this.anet_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B492 <- L691-L691
    this.anet_leaf[:, :, :] = _clm_varcon.spval
    # B493 <- L692-L692
    this.rd_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B494 <- L692-L692
    this.rd_leaf[:, :, :] = _clm_varcon.spval
    # B495 <- L693-L693
    this.ci_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B496 <- L693-L693
    this.ci_leaf[:, :, :] = _clm_varcon.spval
    # B497 <- L694-L694
    this.cs_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B498 <- L694-L694
    this.cs_leaf[:, :, :] = _clm_varcon.spval
    # B499 <- L696-L696
    this.lwp_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B500 <- L696-L696
    this.lwp_leaf[:, :, :] = _clm_varcon.spval
    # B501 <- L697-L697
    this.lwp_bef_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B502 <- L697-L697
    this.lwp_bef_leaf[:, :, :] = _clm_varcon.spval
    # B503 <- L698-L698
    this.dlwp_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF, _mlc.NRK), dtype=np.float64)
    # B504 <- L698-L698
    this.dlwp_leaf[:, :, :, :] = _clm_varcon.spval
    # B505 <- L699-L699
    this.lwp_hist_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B506 <- L699-L699
    this.lwp_hist_leaf[:, :, :] = _clm_varcon.spval
    # B507 <- L700-L700
    this.hs_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B508 <- L700-L700
    this.hs_leaf[:, :, :] = _clm_varcon.spval
    # B509 <- L701-L701
    this.vpd_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B510 <- L701-L701
    this.vpd_leaf[:, :, :] = _clm_varcon.spval
    # B511 <- L702-L702
    this.gs_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B512 <- L702-L702
    this.gs_leaf[:, :, :] = _clm_varcon.spval
    # B513 <- L703-L703
    this.gspot_leaf = np.empty(((endp) - (begp) + 1, NLEVMLCAN, NLEAF), dtype=np.float64)
    # B514 <- L703-L703
    this.gspot_leaf[:, :, :] = _clm_varcon.spval
    return

def inithistory(this, bounds):
    """L708-L736 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    begp = 0
    endp = 0
    # B001 <- L724-L724
    begp = int(bounds.begp)
    # B002 <- L724-L724
    endp = int(bounds.endp)
    # B003 <- L726-L726
    this.gppveg_canopy[begp - 1:endp] = _clm_varcon.spval
    # B004 <- L727-L729
    pass  # hist_addfld1d (infra stub)
    # B005 <- L731-L731
    this.lwp_mean_profile[begp - 1:endp, 0:NLEVMLCAN] = _clm_varcon.spval
    # B006 <- L732-L734
    pass  # hist_addfld2d (infra stub)
    return

def initcold(this, bounds):
    """L739-L771 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    p = 0
    ic = 0
    # B001 <- L763-L769
    for p in range(bounds.begp, bounds.endp + 1):
        for ic in range(1, NLEVMLCAN + 1):
            this.lwp_leaf[p - 1, ic - 1, ISUN - 1] = (-F_0P1)
            this.lwp_leaf[p - 1, ic - 1, ISHA - 1] = (-F_0P1)
            this.h2ocan_profile[p - 1, ic - 1] = 0.0
    return

def restart(this, bounds, ncid, flag):
    """L774-L807 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    readvar = False
    # B001 <- L795-L797
    pass  # restartvar (infra stub)
    return ncid
