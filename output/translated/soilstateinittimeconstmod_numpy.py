"""Machine-translated from SoilStateInitTimeConstMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call soilstateinittimeconst before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
from typing import Any

import numpy as np

from soilstateinittimeconstmod_constants import *  # noqa: F401,F403
from soilstateinittimeconstmod_use_constants import *  # noqa: F401,F403
import abortutils_numpy as _abortutils
import clm_varcon_numpy as _clm_varcon
import clm_varctl_numpy as _clm_varctl
import clm_varpar_numpy as _clm_varpar
import columntype_numpy as _columntype
import decompmod_numpy as _decompmod
import patchtype_numpy as _patchtype
import pftconmod_numpy as _pftconmod
import shr_kind_mod_numpy as _shr_kind_mod
import soilstatetype_numpy as _soi
import soilstatetype_numpy as _soilstatetype
import soiltexmod_numpy as _soiltexmod
import towerdatamod_numpy as _tow
import towerdatamod_numpy as _towerdatamod

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'soilstateinittimeconst': {'kind': 'subroutine', 'args': [{'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'soilstate_inst', 'dtype': 'UNKNOWN(TYPE(SOILSTATE_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}}

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

def _make_patch_type():
    """factory for type(patch_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.column = None
    o.gridcell = None
    o.itype = None
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


def soilstateinittimeconst(bounds, soilstate_inst):
    """L28-L287 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    organic_max = np.float64('130.')
    zsapric = np.float64('0.5')
    pcalpha = np.float64('0.5')
    pcbeta = np.float64('0.139')
    m_to_cm = np.float64('1.E2')
    p = 0
    c = 0
    j = 0
    tex = 0
    m = 0
    clay = 0.0
    sand = 0.0
    om_frac = 0.0
    om_frac_therm = 0.0
    perc_frac = 0.0
    perc_norm = 0.0
    uncon_hksat = 0.0
    uncon_frac = 0.0
    bulk_dens_min = 0.0
    tkdry_min = 0.0
    tksol_min = 0.0
    tkm = 0.0
    cvsol = 0.0
    om_watsat = 0.0
    om_sucsat = 0.0
    om_hksat = 0.0
    om_b = 0.0
    om_cvsol = 0.0
    om_tkdry = 0.0
    om_tksol = 0.0
    beta = 0.0
    # B001 <- L82-L286
    rootprof_beta = _pftconmod.pftcon.rootprof_beta
    z = _columntype.col.z
    zi = _columntype.col.zi
    nbedrock = _columntype.col.nbedrock
    rootfr = soilstate_inst.rootfr_patch
    cellsand = soilstate_inst.cellsand_col
    cellclay = soilstate_inst.cellclay_col
    cellorg = soilstate_inst.cellorg_col
    watsat = soilstate_inst.watsat_col
    sucsat = soilstate_inst.sucsat_col
    hksat = soilstate_inst.hksat_col
    bsw = soilstate_inst.bsw_col
    tkmg = soilstate_inst.tkmg_col
    tkdry = soilstate_inst.tkdry_col
    csol = soilstate_inst.csol_col
    for p in range(bounds.begp, bounds.endp + 1):
        c = _patchtype.patch.column[p - 1]
        beta = rootprof_beta[(_patchtype.patch.itype[p - 1]) - (0)]
        for j in range(1, NLEVSOI + 1):
            rootfr[p - 1, j - 1] = (((beta ** ((zi[c - 1, (j - 1) - 1] * m_to_cm))) - (beta ** ((zi[c - 1, j - 1] * m_to_cm)))))
        for j in range((NLEVSOI + 1), NLEVGRND + 1):
            rootfr[p - 1, j - 1] = 0.0
        for j in range(1, nbedrock[c - 1] + 1):
            rootfr[p - 1, j - 1] = (rootfr[p - 1, j - 1] + (np.sum(rootfr[p - 1, (nbedrock[c - 1] + 1) - 1:NLEVSOI]) / np.float64(nbedrock[c - 1])))
        rootfr[p - 1, (nbedrock[c - 1] + 1) - 1:NLEVSOI] = 0.0
    for c in range(bounds.begc, bounds.endc + 1):
        om_frac = (_tow.tower_organic[_tow.tower_num - 1] / organic_max)
        if ((_tow.tower_clay[_tow.tower_num - 1] >= 0.0) and (_tow.tower_sand[_tow.tower_num - 1] >= 0.0)):
            tex = 0
            clay = _tow.tower_clay[_tow.tower_num - 1]
            sand = _tow.tower_sand[_tow.tower_num - 1]
        else:
            tex = 0
            for m in range(1, _soiltexmod.NTEX + 1):
                if (_tow.tower_tex[_tow.tower_num - 1] == _soiltexmod.soil_tex[m - 1]):
                    tex = m
                    break
                else:
                    continue
            if (tex == 0):
                pass  # write(iulog,...) log — no dataflow
                raise RuntimeError('endrun')  # endrun (infra stub)
            clay = (_soiltexmod.clay_tex[tex - 1] * F_100P)
            sand = (_soiltexmod.sand_tex[tex - 1] * F_100P)
        for j in range(1, NLEVGRND + 1):
            if (z[c - 1, j - 1] > 0.5):
                om_frac = 0.0
            if (j <= NLEVSOI):
                cellsand[c - 1, j - 1] = sand
                cellclay[c - 1, j - 1] = clay
                cellorg[c - 1, j - 1] = (om_frac * organic_max)
            if (tex == 0):
                watsat[c - 1, j - 1] = (F_0P489 - (F_0P00126 * sand))
                sucsat[c - 1, j - 1] = (F_10P * ((F_10P ** ((F_1P88 - (F_0P0131 * sand))))))
                hksat[c - 1, j - 1] = (F_0P0070556 * ((F_10P ** (((-F_0P884) + (F_0P0153 * sand))))))
                bsw[c - 1, j - 1] = (F_2P91 + (F_0P159 * clay))
            else:
                watsat[c - 1, j - 1] = _soiltexmod.watsat_tex[tex - 1]
                sucsat[c - 1, j - 1] = (-_soiltexmod.smpsat_tex[tex - 1])
                hksat[c - 1, j - 1] = (_soiltexmod.hksat_tex[tex - 1] / F_60P)
                bsw[c - 1, j - 1] = _soiltexmod.bsw_tex[tex - 1]
            om_watsat = _f_max((F_0P93 - (F_0P1 * ((z[c - 1, j - 1] / zsapric)))), F_0P83)
            om_sucsat = _f_min((F_10P3 - (F_0P2 * ((z[c - 1, j - 1] / zsapric)))), F_10P1)
            om_hksat = _f_max((F_0P28 - (F_0P2799 * ((z[c - 1, j - 1] / zsapric)))), hksat[c - 1, j - 1])
            om_b = _f_min((F_2P7 + (F_9P3 * ((z[c - 1, j - 1] / zsapric)))), F_12P0)
            watsat[c - 1, j - 1] = ((((1.0 - om_frac)) * watsat[c - 1, j - 1]) + (om_watsat * om_frac))
            sucsat[c - 1, j - 1] = ((((1.0 - om_frac)) * sucsat[c - 1, j - 1]) + (om_sucsat * om_frac))
            bsw[c - 1, j - 1] = ((((1.0 - om_frac)) * bsw[c - 1, j - 1]) + (om_frac * om_b))
            if (om_frac > pcalpha):
                perc_norm = (((1.0 - pcalpha)) ** ((-pcbeta)))
                perc_frac = (perc_norm * (((om_frac - pcalpha)) ** pcbeta))
            else:
                perc_frac = 0.0
            uncon_frac = (((1.0 - om_frac)) + (((1.0 - perc_frac)) * om_frac))
            if (om_frac < 1.0):
                uncon_hksat = (uncon_frac / (((((1.0 - om_frac)) / hksat[c - 1, j - 1]) + (((((1.0 - perc_frac)) * om_frac)) / om_hksat))))
            else:
                uncon_hksat = 0.0
            hksat[c - 1, j - 1] = ((uncon_frac * uncon_hksat) + (((perc_frac * om_frac)) * om_hksat))
            om_frac_therm = om_frac
            om_tkdry = F_0P05
            if (j <= NLEVSOI):
                bulk_dens_min = (F_2700P * ((1.0 - watsat[c - 1, j - 1])))
                tkdry_min = ((((F_0P135 * bulk_dens_min) + F_64P7)) / ((F_2700P - (F_0P947 * bulk_dens_min))))
                tkdry[c - 1, j - 1] = ((((1.0 - om_frac_therm)) * tkdry_min) + (om_frac_therm * om_tkdry))
            else:
                bulk_dens_min = F_2700P
                tkdry_min = ((((F_0P135 * bulk_dens_min) + F_64P7)) / ((F_2700P - (F_0P947 * bulk_dens_min))))
                tkdry[c - 1, j - 1] = tkdry_min
            om_tksol = F_0P25
            if (j <= NLEVSOI):
                tksol_min = ((((F_8P80 * sand) + (F_2P92 * clay))) / ((sand + clay)))
                tkm = ((((1.0 - om_frac_therm)) * tksol_min) + (om_frac_therm * om_tksol))
                tkmg[c - 1, j - 1] = (tkm ** ((1.0 - watsat[c - 1, j - 1])))
            else:
                tkmg[c - 1, j - 1] = F_3P
            if (tex == 0):
                cvsol = ((((((F_2P128 * sand) + (F_2P385 * clay))) / ((sand + clay)))) * F_1PE6)
            else:
                cvsol = F_1P926E06
            om_cvsol = F_2P5E06
            if (j <= NLEVSOI):
                csol[c - 1, j - 1] = ((((1.0 - om_frac_therm)) * cvsol) + (om_frac_therm * om_cvsol))
            else:
                csol[c - 1, j - 1] = CSOL_BEDROCK
    return soilstate_inst
