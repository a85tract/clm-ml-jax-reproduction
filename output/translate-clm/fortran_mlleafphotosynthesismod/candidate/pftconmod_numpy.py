"""Machine-translated from pftconMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call init before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
from typing import Any

import numpy as np

from pftconmod_constants import *  # noqa: F401,F403
from pftconmod_use_constants import *  # noqa: F401,F403
import clm_varctl_numpy as _clm_varctl
import clm_varpar_numpy as _clm_varpar
import mlclm_varctl_numpy as _mlc
import mlclm_varctl_numpy as _mlclm_varctl
import shr_kind_mod_numpy as _shr_kind_mod

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'init': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(PFTCON_TYPE))', 'intent': 'UNKNOWN', 'optional': False}], 'result': None, 'result_dtype': None}, 'initallocate': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(PFTCON_TYPE))', 'intent': 'UNKNOWN', 'optional': False}], 'result': None, 'result_dtype': None}, 'initread': {'kind': 'subroutine', 'args': [{'name': 'this', 'dtype': 'UNKNOWN(CLASS(PFTCON_TYPE))', 'intent': 'UNKNOWN', 'optional': False}], 'result': None, 'result_dtype': None}}

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

def _make_pftcon_type():
    """factory for type(pftcon_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.dleaf = None
    o.c3psn = None
    o.xl = None
    o.rhol = None
    o.rhos = None
    o.taul = None
    o.taus = None
    o.rootprof_beta = None
    o.slatop = None
    return o

pftcon = _make_pftcon_type()  # module state (UNKNOWN(TYPE(PFTCON_TYPE))), set by init

def init(this):
    """L48-L55 subroutine (machine-translated)."""
    # B001 <- L52-L52 AGENT_QUEUE: call to external subroutine 'this % initallocate'
    raise NotImplementedError("call to external subroutine 'this % initallocate'")  # B001
    # B002 <- L53-L53 AGENT_QUEUE: call to external subroutine 'this % initread'
    raise NotImplementedError("call to external subroutine 'this % initread'")  # B002
    return

def initallocate(this):
    """L58-L78 subroutine (machine-translated)."""
    # B001 <- L68-L68
    this.dleaf = np.empty(((_clm_varpar.MXPFT) - (0) + 1,), dtype=np.float64)
    # B002 <- L69-L69
    this.c3psn = np.empty(((_clm_varpar.MXPFT) - (0) + 1,), dtype=np.float64)
    # B003 <- L70-L70
    this.xl = np.empty(((_clm_varpar.MXPFT) - (0) + 1,), dtype=np.float64)
    # B004 <- L71-L71
    this.rhol = np.empty(((_clm_varpar.MXPFT) - (0) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B005 <- L72-L72
    this.rhos = np.empty(((_clm_varpar.MXPFT) - (0) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B006 <- L73-L73
    this.taul = np.empty(((_clm_varpar.MXPFT) - (0) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B007 <- L74-L74
    this.taus = np.empty(((_clm_varpar.MXPFT) - (0) + 1, _clm_varpar.NUMRAD), dtype=np.float64)
    # B008 <- L75-L75
    this.rootprof_beta = np.empty(((_clm_varpar.MXPFT) - (0) + 1,), dtype=np.float64)
    # B009 <- L76-L76
    this.slatop = np.empty(((_clm_varpar.MXPFT) - (0) + 1,), dtype=np.float64)
    return

def initread(this):
    """L81-L304 subroutine (machine-translated)."""
    # B001 <- L175-L175
    this.dleaf[:] = (-F_999P)
    # B002 <- L176-L176
    this.dleaf[0:I_16] = F_0P04
    # B003 <- L180-L180
    this.c3psn[:] = (-F_999P)
    # B004 <- L181-L181
    this.c3psn[0:I_13] = 1.0
    # B005 <- L182-L182
    this.c3psn[I_14 - 1:I_14] = 0.0
    # B006 <- L183-L183
    this.c3psn[I_15 - 1:I_16] = 1.0
    # B007 <- L187-L187
    this.xl[:] = (-F_999P)
    # B008 <- L188-L188
    this.xl[0:I_3] = F_0P01
    # B009 <- L189-L189
    this.xl[I_4 - 1:I_5] = F_0P10
    # B010 <- L190-L190
    this.xl[I_6 - 1:I_6] = F_0P01
    # B011 <- L191-L191
    this.xl[I_7 - 1:I_8] = F_0P25
    # B012 <- L192-L192
    this.xl[I_9 - 1:I_9] = F_0P01
    # B013 <- L193-L193
    this.xl[I_10 - 1:I_11] = F_0P25
    # B014 <- L194-L194
    this.xl[I_12 - 1:I_16] = (-F_0P30)
    # B015 <- L198-L198
    this.rhol[:, :] = (-F_999P)
    # B016 <- L200-L200
    this.rhol[0:I_3, _clm_varpar.IVIS - 1] = F_0P07
    # B017 <- L201-L201
    this.rhol[I_4 - 1:I_8, _clm_varpar.IVIS - 1] = F_0P10
    # B018 <- L202-L202
    this.rhol[I_9 - 1:I_9, _clm_varpar.IVIS - 1] = F_0P07
    # B019 <- L203-L203
    this.rhol[I_10 - 1:I_11, _clm_varpar.IVIS - 1] = F_0P10
    # B020 <- L204-L204
    this.rhol[I_12 - 1:I_16, _clm_varpar.IVIS - 1] = F_0P11
    # B021 <- L206-L206
    this.rhol[0:I_3, _clm_varpar.INIR - 1] = F_0P35
    # B022 <- L207-L207
    this.rhol[I_4 - 1:I_8, _clm_varpar.INIR - 1] = F_0P45
    # B023 <- L208-L208
    this.rhol[I_9 - 1:I_9, _clm_varpar.INIR - 1] = F_0P35
    # B024 <- L209-L209
    this.rhol[I_10 - 1:I_11, _clm_varpar.INIR - 1] = F_0P45
    # B025 <- L210-L210
    this.rhol[I_12 - 1:I_16, _clm_varpar.INIR - 1] = F_0P35
    # B026 <- L214-L214
    this.rhos[:, :] = (-F_999P)
    # B027 <- L216-L216
    this.rhos[0:I_11, _clm_varpar.IVIS - 1] = F_0P16
    # B028 <- L217-L217
    this.rhos[I_12 - 1:I_16, _clm_varpar.IVIS - 1] = F_0P31
    # B029 <- L219-L219
    this.rhos[0:I_11, _clm_varpar.INIR - 1] = F_0P39
    # B030 <- L220-L220
    this.rhos[I_12 - 1:I_16, _clm_varpar.INIR - 1] = F_0P53
    # B031 <- L224-L224
    this.taul[:, :] = (-F_999P)
    # B032 <- L226-L226
    this.taul[0:I_16, _clm_varpar.IVIS - 1] = F_0P05
    # B033 <- L228-L228
    this.taul[0:I_3, _clm_varpar.INIR - 1] = F_0P10
    # B034 <- L229-L229
    this.taul[I_4 - 1:I_8, _clm_varpar.INIR - 1] = F_0P25
    # B035 <- L230-L230
    this.taul[I_9 - 1:I_9, _clm_varpar.INIR - 1] = F_0P10
    # B036 <- L231-L231
    this.taul[I_10 - 1:I_11, _clm_varpar.INIR - 1] = F_0P25
    # B037 <- L232-L232
    this.taul[I_12 - 1:I_16, _clm_varpar.INIR - 1] = F_0P34
    # B038 <- L236-L236
    this.taus[:, :] = (-F_999P)
    # B039 <- L238-L238
    this.taus[0:I_11, _clm_varpar.IVIS - 1] = F_0P001
    # B040 <- L239-L239
    this.taus[I_12 - 1:I_16, _clm_varpar.IVIS - 1] = F_0P12
    # B041 <- L241-L241
    this.taus[0:I_11, _clm_varpar.INIR - 1] = F_0P001
    # B042 <- L242-L242
    this.taus[I_12 - 1:I_16, _clm_varpar.INIR - 1] = F_0P25
    # B043 <- L246-L246
    this.rootprof_beta[:] = (-F_999P)
    # B044 <- L247-L247
    this.rootprof_beta[0:1] = F_0P976
    # B045 <- L248-L248
    this.rootprof_beta[1:I_3] = F_0P943
    # B046 <- L249-L249
    this.rootprof_beta[I_4 - 1:I_4] = F_0P993
    # B047 <- L250-L250
    this.rootprof_beta[I_5 - 1:I_5] = F_0P966
    # B048 <- L251-L251
    this.rootprof_beta[I_6 - 1:I_6] = F_0P993
    # B049 <- L252-L252
    this.rootprof_beta[I_7 - 1:I_7] = F_0P966
    # B050 <- L253-L253
    this.rootprof_beta[I_8 - 1:I_8] = F_0P943
    # B051 <- L254-L254
    this.rootprof_beta[I_9 - 1:I_10] = F_0P964
    # B052 <- L255-L255
    this.rootprof_beta[I_11 - 1:I_12] = F_0P914
    # B053 <- L256-L256
    this.rootprof_beta[I_13 - 1:I_16] = F_0P943
    # B054 <- L260-L260
    this.slatop[:] = (-F_999P)
    # B055 <- L261-L261
    this.slatop[0] = F_0P010
    # B056 <- L262-L262
    this.slatop[1] = F_0P008
    # B057 <- L263-L263
    this.slatop[2] = F_0P024
    # B058 <- L264-L264
    this.slatop[I_4 - 1] = F_0P012
    # B059 <- L265-L265
    this.slatop[I_5 - 1] = F_0P012
    # B060 <- L266-L266
    this.slatop[I_6 - 1] = F_0P030
    # B061 <- L267-L267
    this.slatop[I_7 - 1] = F_0P030
    # B062 <- L268-L268
    this.slatop[I_8 - 1] = F_0P030
    # B063 <- L269-L269
    this.slatop[I_9 - 1] = F_0P012
    # B064 <- L270-L270
    this.slatop[I_10 - 1] = F_0P030
    # B065 <- L271-L271
    this.slatop[I_11 - 1] = F_0P030
    # B066 <- L272-L272
    this.slatop[I_12 - 1] = F_0P030
    # B067 <- L273-L273
    this.slatop[I_13 - 1] = F_0P030
    # B068 <- L274-L274
    this.slatop[I_14 - 1] = F_0P030
    # B069 <- L275-L275
    this.slatop[I_15 - 1] = F_0P030
    # B070 <- L276-L276
    this.slatop[I_16 - 1] = F_0P030
    # B071 <- L280-L302
    if (_mlc.pftcon_val == 1):
        pass  # write(iulog,...) log — no dataflow
        this.xl[I_7 - 1] = F_0P53
        this.rhol[I_7 - 1, _clm_varpar.IVIS - 1] = F_0P06
        this.rhol[I_7 - 1, _clm_varpar.INIR - 1] = F_0P42
        this.rhos[I_7 - 1, _clm_varpar.IVIS - 1] = F_0P21
        this.rhos[I_7 - 1, _clm_varpar.INIR - 1] = F_0P49
        this.taul[I_7 - 1, _clm_varpar.IVIS - 1] = F_0P04
        this.taul[I_7 - 1, _clm_varpar.INIR - 1] = F_0P43
    return
