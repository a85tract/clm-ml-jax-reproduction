"""Machine-translated from MLPlantHydraulicsMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call plantresistance before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
from typing import Any

import numpy as np

from mlplanthydraulicsmod_constants import *  # noqa: F401,F403
from mlplanthydraulicsmod_use_constants import *  # noqa: F401,F403
import abortutils_numpy as _abortutils
import clm_varcon_numpy as _clm_varcon
import clm_varctl_numpy as _clm_varctl
import clm_varpar_numpy as _clm_varpar
import columntype_numpy as _columntype
import mlcanopyfluxestype_numpy as _mlc
import mlcanopyfluxestype_numpy as _mlcanopyfluxestype
import mlclm_varcon_numpy as _mlclm_varcon
import mlclm_varctl_numpy as _mlclm_varctl
import mlpftconmod_numpy as _mlp
import mlpftconmod_numpy as _mlpftconmod
import patchtype_numpy as _patchtype
import shr_kind_mod_numpy as _shr_kind_mod
import soilstatetype_numpy as _soi
import soilstatetype_numpy as _soilstatetype
import waterstatebulktype_numpy as _wat
import waterstatebulktype_numpy as _waterstatebulktype

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'plantresistance': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'soilresistance': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'soilstate_inst', 'dtype': 'UNKNOWN(TYPE(SOILSTATE_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'waterstatebulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERSTATEBULK_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'leafwaterpotential': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}}

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

def _make_mlpftcon_type():
    """factory for type(mlpftcon_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.vcmaxpft = None
    o.gplant_spa = None
    o.capac_spa = None
    o.iota_spa = None
    o.root_radius_spa = None
    o.root_density_spa = None
    o.root_resist_spa = None
    o.gsmin_spa = None
    o.g0_bb = None
    o.g1_bb = None
    o.g0_med = None
    o.g1_med = None
    o.psi50_gs = None
    o.shape_gs = None
    o.emleaf = None
    o.clump_fac = None
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


def plantresistance(num_filter, filter, mlcanopy_inst):
    """L25-L86 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    ic = 0
    rplant = 0.0
    # B001 <- L48-L85
    gplant_spa = _mlp.mlpftcon.gplant_spa
    ncan = mlcanopy_inst.ncan_canopy
    rsoil = mlcanopy_inst.rsoil_soil
    dpai = mlcanopy_inst.dpai_profile
    zs = mlcanopy_inst.zs_profile
    lsc = mlcanopy_inst.lsc_profile
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                rplant = (1.0 / gplant_spa[(_patchtype.patch.itype[p - 1]) - (0)])
                lsc[p - 1, ic - 1] = (1.0 / ((rsoil[p - 1] + rplant)))
            else:
                lsc[p - 1, ic - 1] = 0.0
    return mlcanopy_inst

def soilresistance(num_filter, filter, soilstate_inst, waterstatebulk_inst, mlcanopy_inst):
    """L89-L257 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    c = 0
    j = 0
    nlayers = 0
    head = 0.0
    root_cross_sec_area = 0.0
    root_biomass_density = 0.0
    root_length_density = 0.0
    root_dist = 0.0
    hk = 0.0
    soilr1 = 0.0
    soilr2 = 0.0
    soilr = 0.0
    smp_mpa = np.empty((NLEVSOI,), dtype=np.float64)
    evap = np.empty((NLEVSOI,), dtype=np.float64)
    totevap = 0.0
    minlwp_spa = 0.0
    # B001 <- L136-L256
    root_radius_spa = _mlp.mlpftcon.root_radius_spa
    root_density_spa = _mlp.mlpftcon.root_density_spa
    root_resist_spa = _mlp.mlpftcon.root_resist_spa
    dz = _columntype.col.dz
    nbedrock = _columntype.col.nbedrock
    smp_l = soilstate_inst.smp_l_col
    hk_l = soilstate_inst.hk_l_col
    rootfr = soilstate_inst.rootfr_patch
    h2osoi_ice = waterstatebulk_inst.h2osoi_ice_col
    lai = mlcanopy_inst.lai_canopy
    root_biomass = mlcanopy_inst.root_biomass_canopy
    psis = mlcanopy_inst.psis_soil
    rsoil = mlcanopy_inst.rsoil_soil
    soil_et_loss = mlcanopy_inst.soil_et_loss_soil
    head = ((DENH2O * GRAV) * F_1PEM06)
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        c = _patchtype.patch.column[p - 1]
        nlayers = int(nbedrock[c - 1])
        root_cross_sec_area = (_clm_varcon.rpi * (root_radius_spa[(_patchtype.patch.itype[p - 1]) - (0)] * root_radius_spa[(_patchtype.patch.itype[p - 1]) - (0)]))
        rsoil[p - 1] = 0.0
        totevap = 0.0
        for j in range(1, nlayers + 1):
            hk = (hk_l[c - 1, j - 1] * ((F_1PEM03 / head)))
            hk = (((hk * DENH2O) / MMH2O) * F_1000P)
            smp_mpa[j - 1] = ((smp_l[c - 1, j - 1] * F_1PEM03) * head)
            root_biomass_density = ((root_biomass[p - 1] * rootfr[p - 1, j - 1]) / dz[c - 1, j - 1])
            root_biomass_density = _f_max(root_biomass_density, F_1PEM10)
            root_length_density = (root_biomass_density / ((root_density_spa[(_patchtype.patch.itype[p - 1]) - (0)] * root_cross_sec_area)))
            root_dist = math.sqrt((1.0 / ((root_length_density * _clm_varcon.rpi))))
            soilr1 = (math.log((root_dist / root_radius_spa[(_patchtype.patch.itype[p - 1]) - (0)])) / (((((F_2P * _clm_varcon.rpi) * root_length_density) * dz[c - 1, j - 1]) * hk)))
            soilr2 = (root_resist_spa[(_patchtype.patch.itype[p - 1]) - (0)] / ((root_biomass_density * dz[c - 1, j - 1])))
            soilr = (soilr1 + soilr2)
            rsoil[p - 1] = (rsoil[p - 1] + (1.0 / soilr))
            evap[j - 1] = (((smp_mpa[j - 1] - minlwp_spa)) / soilr)
            evap[j - 1] = _f_max(evap[j - 1], 0.0)
            if (h2osoi_ice[c - 1, j - 1] > 0.0):
                evap[j - 1] = 0.0
            totevap = (totevap + evap[j - 1])
        rsoil[p - 1] = (lai[p - 1] / rsoil[p - 1])
        psis[p - 1] = 0.0
        soil_et_loss[p - 1, :] = 0.0
        for j in range(1, nlayers + 1):
            psis[p - 1] = (psis[p - 1] + (smp_mpa[j - 1] * evap[j - 1]))
            if (totevap > 0.0):
                soil_et_loss[p - 1, j - 1] = (evap[j - 1] / totevap)
            else:
                soil_et_loss[p - 1, j - 1] = (1.0 / nlayers)
        if (totevap > 0.0):
            psis[p - 1] = (psis[p - 1] / totevap)
        else:
            psis[p - 1] = minlwp_spa
    return mlcanopy_inst

def leafwaterpotential(num_filter, filter, il, mlcanopy_inst):
    """L260-L332 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    ic = 0
    head = 0.0
    dtime = 0.0
    y0 = 0.0
    dy = 0.0
    a = 0.0
    b = 0.0
    # B001 <- L290-L331
    capac_spa = _mlp.mlpftcon.capac_spa
    ncan = mlcanopy_inst.ncan_canopy
    psis = mlcanopy_inst.psis_soil
    dpai = mlcanopy_inst.dpai_profile
    zs = mlcanopy_inst.zs_profile
    lsc = mlcanopy_inst.lsc_profile
    trleaf = mlcanopy_inst.trleaf_leaf
    lwp_bef = mlcanopy_inst.lwp_bef_leaf
    lwp = mlcanopy_inst.lwp_leaf
    head = ((DENH2O * GRAV) * F_1PEM06)
    dtime = DTIME_ML
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                y0 = lwp_bef[p - 1, ic - 1, il - 1]
                a = ((psis[p - 1] - (head * zs[p - 1, ic - 1])) - ((F_1000P * trleaf[p - 1, ic - 1, il - 1]) / lsc[p - 1, ic - 1]))
                b = (capac_spa[(_patchtype.patch.itype[p - 1]) - (0)] / lsc[p - 1, ic - 1])
                dy = (((a - y0)) * ((1.0 - math.exp((-(dtime / b))))))
                lwp[p - 1, ic - 1, il - 1] = (y0 + dy)
            else:
                lwp[p - 1, ic - 1, il - 1] = 0.0
    return mlcanopy_inst


# Flattened adapters for the differential gate (recast-clm, flatten.py).
class _Record:
    def __init__(self, **fields):
        self.__dict__.update(fields)

def plantresistance_flat(num_filter, filter, np_, mlcanopy_inst__dpai_profile, mlcanopy_inst__lsc_profile, mlcanopy_inst__ncan_canopy, mlcanopy_inst__rsoil_soil, mlcanopy_inst__zs_profile, mlpftcon__gplant_spa, patch__itype):
    mlcanopy_inst = _Record(dpai_profile=mlcanopy_inst__dpai_profile, lsc_profile=mlcanopy_inst__lsc_profile, ncan_canopy=mlcanopy_inst__ncan_canopy, rsoil_soil=mlcanopy_inst__rsoil_soil, zs_profile=mlcanopy_inst__zs_profile)
    import mlpftconmod_numpy as _mlpftconmod
    if not hasattr(getattr(_mlpftconmod, 'mlpftcon', None), '__dict__'):
        _mlpftconmod.mlpftcon = _Record()
    _mlpftconmod.mlpftcon.gplant_spa = mlpftcon__gplant_spa
    import patchtype_numpy as _patchtype
    if not hasattr(getattr(_patchtype, 'patch', None), '__dict__'):
        _patchtype.patch = _Record()
    _patchtype.patch.itype = patch__itype
    _out = plantresistance(num_filter=num_filter, filter=filter, mlcanopy_inst=mlcanopy_inst)
    _out = (_out,)
    mlcanopy_inst_, = _out
    mlcanopy_inst__lsc_profile = mlcanopy_inst.lsc_profile
    return mlcanopy_inst__lsc_profile

def leafwaterpotential_flat(num_filter, filter, il, np_, mlcanopy_inst__dpai_profile, mlcanopy_inst__lsc_profile, mlcanopy_inst__lwp_bef_leaf, mlcanopy_inst__lwp_leaf, mlcanopy_inst__ncan_canopy, mlcanopy_inst__psis_soil, mlcanopy_inst__trleaf_leaf, mlcanopy_inst__zs_profile, mlpftcon__capac_spa, patch__itype):
    mlcanopy_inst = _Record(dpai_profile=mlcanopy_inst__dpai_profile, lsc_profile=mlcanopy_inst__lsc_profile, lwp_bef_leaf=mlcanopy_inst__lwp_bef_leaf, lwp_leaf=mlcanopy_inst__lwp_leaf, ncan_canopy=mlcanopy_inst__ncan_canopy, psis_soil=mlcanopy_inst__psis_soil, trleaf_leaf=mlcanopy_inst__trleaf_leaf, zs_profile=mlcanopy_inst__zs_profile)
    import mlpftconmod_numpy as _mlpftconmod
    if not hasattr(getattr(_mlpftconmod, 'mlpftcon', None), '__dict__'):
        _mlpftconmod.mlpftcon = _Record()
    _mlpftconmod.mlpftcon.capac_spa = mlpftcon__capac_spa
    import patchtype_numpy as _patchtype
    if not hasattr(getattr(_patchtype, 'patch', None), '__dict__'):
        _patchtype.patch = _Record()
    _patchtype.patch.itype = patch__itype
    _out = leafwaterpotential(num_filter=num_filter, filter=filter, il=il, mlcanopy_inst=mlcanopy_inst)
    _out = (_out,)
    mlcanopy_inst_, = _out
    mlcanopy_inst__lwp_leaf = mlcanopy_inst.lwp_leaf
    return mlcanopy_inst__lwp_leaf

_SIGNATURES.update({
    'plantresistance_flat': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'num_filter'}]}, {'name': 'np_', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlcanopy_inst__dpai_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lsc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__ncan_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rsoil_soil', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zs_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlpftcon__gplant_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'patch__itype', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}], 'result': None, 'result_dtype': None},
    'leafwaterpotential_flat': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'num_filter'}]}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'np_', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlcanopy_inst__dpai_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lsc_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lwp_bef_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lwp_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ncan_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__psis_soil', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__trleaf_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__zs_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlpftcon__capac_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'patch__itype', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}], 'result': None, 'result_dtype': None},
})


# Input domains for the differential gate (recast-clm, domains.py).
# Generated inputs only; recorded inputs never pass through here.
def _PREPARE_INPUTS(name, inputs, rng):
    if 'il' in inputs:
        inputs['il'] = np.int32(rng.integers(1, 3))

