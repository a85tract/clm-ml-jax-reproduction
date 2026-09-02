"""Machine-translated from clm_time_manager.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call get_step_size before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
import re as _re
from typing import Any

import numpy as np

from clm_time_manager_constants import *  # noqa: F401,F403

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'get_step_size': {'kind': 'function', 'args': [], 'result': 'get_step_size', 'result_dtype': 'int32'}, 'get_nstep': {'kind': 'function', 'args': [], 'result': 'get_nstep', 'result_dtype': 'int32'}, 'isleap': {'kind': 'function', 'args': [{'name': 'year', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'calendar', 'dtype': 'str', 'intent': 'IN', 'optional': False}], 'result': 'isleap', 'result_dtype': 'bool'}, 'get_curr_date': {'kind': 'subroutine', 'args': [{'name': 'yr', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}, {'name': 'mon', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}, {'name': 'day', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}, {'name': 'tod', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'get_prev_date': {'kind': 'subroutine', 'args': [{'name': 'yr', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}, {'name': 'mon', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}, {'name': 'day', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}, {'name': 'tod', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'get_curr_time': {'kind': 'subroutine', 'args': [{'name': 'days', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}, {'name': 'seconds', 'dtype': 'int32', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'get_curr_calday': {'kind': 'function', 'args': [{'name': 'offset', 'dtype': 'int32', 'intent': 'IN', 'optional': True}], 'result': 'get_curr_calday', 'result_dtype': 'float64'}, 'get_prev_calday': {'kind': 'function', 'args': [], 'result': 'get_prev_calday', 'result_dtype': 'float64'}, 'is_end_curr_day': {'kind': 'function', 'args': [], 'result': 'is_end_curr_day', 'result_dtype': 'bool'}, 'is_end_curr_month': {'kind': 'function', 'args': [], 'result': 'is_end_curr_month', 'result_dtype': 'bool'}}

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


_FMT_TOKEN = _re.compile(
    r"\s*(?:(?P<rep>\d+)?\s*(?P<ed>I\d+(?:\.\d+)?|F\d+\.\d+"
    r"|E[SN]?\d+\.\d+(?:E\d+)?|G\d+\.\d+|A(?:\d+)?|L\d+|\d*X|/"
    r"|'[^']*'|\"[^\"]*\"))\s*,?",
    _re.I,
)


def _f_fmt_write(fmt: str, *vals: Any) -> str:
    """Formatted internal WRITE (#16), for the edit descriptors the corpus
    uses: ``Iw[.m]``, ``Fw.d``, ``Ew.d`` / ``ESw.d``, ``Gw.d``, ``A[w]``,
    ``Lw``, ``nX``, ``/``, literals, repeat counts. Fortran field semantics:
    right-justified, asterisks on overflow, ``Iw.m`` zero-filled to ``m``
    digits, ``E`` as ``0.dddE+ee``."""
    body = fmt.strip()
    if body.startswith("(") and body.endswith(")"):
        body = body[1:-1]
    out: list[str] = []
    values = list(vals)
    pos = 0
    while pos < len(body):
        m = _FMT_TOKEN.match(body, pos)
        if not m or m.end() == pos:
            raise ValueError(f"_f_fmt_write: cannot parse {fmt!r}")
        pos = m.end()
        rep = int(m.group("rep")) if m.group("rep") else 1
        ed = m.group("ed")
        for _ in range(rep):
            u = ed.upper()
            if u.startswith(("'", '"')):
                out.append(ed[1:-1])
            elif u.endswith("X"):
                out.append(" " * (int(u[:-1]) if u[:-1] else 1))
            elif u == "/":
                out.append("\n")
            else:
                if not values:
                    return "".join(out)
                out.append(_fmt_one(u, values.pop(0)))
    return "".join(out)


def _fmt_one(u: str, v: Any) -> str:
    def fit(s: str, w: int) -> str:
        return s.rjust(w) if len(s) <= w else "*" * w

    if u[0] == "I":
        width, _, minimum = u[1:].partition(".")
        iv = int(v)
        digits = str(abs(iv))
        if minimum:
            digits = digits.rjust(int(minimum), "0")
        return fit(("-" if iv < 0 else "") + digits, int(width))
    if u[0] == "F":
        width, decimals = u[1:].split(".")
        s = f"{float(v):.{int(decimals)}f}"
        if s.startswith("0.") and len(s) > int(width):
            s = s[1:]
        elif s.startswith("-0.") and len(s) > int(width):
            s = "-" + s[2:]
        return fit(s, int(width))
    if u[0] == "E":
        sci = u.startswith("ES")
        spec = u[2:] if u.startswith(("ES", "EN")) else u[1:]
        wd, _, ee = spec.partition("E")
        w, d = (int(x) for x in wd.split("."))
        ew = int(ee) if ee else 2
        x = float(v)
        if x == 0.0:
            mant, exp = 0.0, 0
        else:
            exp = int(np.floor(np.log10(abs(x))))
            if sci:
                mant = round(x / 10.0**exp, d)
                if abs(mant) >= 10.0:
                    mant /= 10.0
                    exp += 1
            else:
                exp += 1
                mant = round(x / 10.0**exp, d)
                if abs(mant) >= 1.0:
                    mant /= 10.0
                    exp += 1
        s = f"{mant:.{d}f}E{'+' if exp >= 0 else '-'}{abs(exp):0{ew}d}"
        return fit(s, w)
    if u[0] == "G":
        width, decimals = u[1:].split(".")
        return fit(f"{float(v):.{int(decimals)}g}", int(width))
    if u[0] == "A":
        s = str(v)
        if len(u) > 1:
            w = int(u[1:])
            return s[:w] if len(s) >= w else s.rjust(w)
        return s
    if u[0] == "L":
        return fit("T" if bool(v) else "F", int(u[1:]))
    raise ValueError(f"_f_fmt_write: descriptor {u}")


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


def _int_bits(*vals: Any) -> int | None:
    """The widest integer KIND among the operands, in bits, or ``None`` when
    none carries a dtype -- a bare literal -- in which case the operation
    stays unbounded, as it always was.

    Fortran's bit intrinsics work on the operand's KIND, 32- or 64-bit two's
    complement; a Python int is unbounded and keeps bits Fortran drops, which
    put ``mt19937_64`` wrong past its first tempering step (#15)."""
    width = None
    for v in vals:
        dt = getattr(v, "dtype", None)
        if dt is not None and np.issubdtype(dt, np.integer):
            b = dt.itemsize * 8
            width = b if width is None else max(width, b)
    return width


def _wrap_signed(v: Any, bits: int | None) -> Any:
    if bits is None:
        return int(v)
    v = int(v) & ((1 << bits) - 1)
    if v >= (1 << (bits - 1)):
        v -= 1 << bits
    return v


def _f_iand(a: Any, b: Any) -> Any:
    bits = _int_bits(a, b)
    m = (1 << bits) - 1 if bits is not None else -1
    return _wrap_signed((int(a) & m) & (int(b) & m), bits)


def _f_ior(a: Any, b: Any) -> Any:
    bits = _int_bits(a, b)
    m = (1 << bits) - 1 if bits is not None else -1
    return _wrap_signed((int(a) & m) | (int(b) & m), bits)


def _f_ieor(a: Any, b: Any) -> Any:
    bits = _int_bits(a, b)
    m = (1 << bits) - 1 if bits is not None else -1
    return _wrap_signed((int(a) & m) ^ (int(b) & m), bits)


def _f_ishft(i: Any, shift: Any) -> Any:
    """Fortran ISHFT: a LOGICAL shift (zero-fill), positive = left, negative
    = right, within the operand's bit width (#15)."""
    s = int(shift)
    bits = _int_bits(i)
    v = int(i)
    if bits is not None:
        v &= (1 << bits) - 1  # the unsigned view, for a logical shift
    r = (v << s) if s >= 0 else (v >> (-s))
    return _wrap_signed(r, bits)


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

dtstep = None  # module state (int32), set by init
itim = None  # module state (int32), set by init
start_date_ymd = None  # module state (int32), set by init
start_date_tod = None  # module state (int32), set by init
curr_date_ymd = None  # module state (int32), set by init
curr_date_tod = None  # module state (int32), set by init

def get_step_size():
    """L104-L112 function (machine-translated)."""
    get_step_size = 0
    # B001 <- L110-L110
    get_step_size = dtstep
    return get_step_size

def get_nstep():
    """L115-L123 function (machine-translated)."""
    get_nstep = 0
    # B001 <- L121-L121
    get_nstep = itim
    return get_nstep

def isleap(year, calendar):
    """L126-L151 function (machine-translated)."""
    isleap = False
    # B001 <- L137-L137
    isleap = False
    # B002 <- L139-L149
    if (_fstr_eq(_f_trim(calendar), 'GREGORIAN')):
        if (_f_mod(year, I_4) == 0):
            isleap = True
            if (_f_mod(year, I_100) == 0):
                isleap = False
                if (_f_mod(year, I_400) == 0):
                    isleap = True
    return isleap

def get_curr_date():
    """L154-L235 subroutine (machine-translated)."""
    global curr_date_ymd
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    yr = 0
    mon = 0
    day = 0
    tod = 0
    nsecs = 0
    ndays = 0
    nyears = 0
    mcyear = 0
    mcmnth = 0
    mcday = 0
    days_per_month = 0
    # B001 <- L178-L178
    mcyear = _f_int_div(start_date_ymd, I_10000)
    # B002 <- L182-L182
    nsecs = (itim * dtstep)
    # B003 <- L183-L183
    ndays = _f_int_div(((nsecs + start_date_tod)), I_86400)
    # B004 <- L184-L188
    if isleap(mcyear, CALKINDFLAG):
        nyears = _f_int_div(ndays, I_366)
    else:
        nyears = _f_int_div(ndays, I_365)
    # B005 <- L193-L197
    if isleap(mcyear, CALKINDFLAG):
        ndays = _f_mod(ndays, I_366)
    else:
        ndays = _f_mod(ndays, I_365)
    # B006 <- L201-L201
    tod = _f_mod((nsecs + start_date_tod), I_86400)
    # B007 <- L205-L205
    mcyear = (_f_int_div(start_date_ymd, I_10000) + nyears)
    # B008 <- L206-L206
    mcmnth = _f_int_div(_f_mod(start_date_ymd, I_10000), I_100)
    # B009 <- L207-L207
    mcday = (_f_mod(start_date_ymd, I_100) + ndays)
    # B010 <- L212-L212
    pass  # continue
    # B011 <- L213-L217
    if isleap(mcyear, CALKINDFLAG):
        days_per_month = MDAYLEAP[mcmnth - 1]
    else:
        days_per_month = MDAY[mcmnth - 1]
    # B012 <- L218-L226 AGENT_QUEUE: goto 10 is not a loop-exit pattern
    raise NotImplementedError('goto 10 is not a loop-exit pattern')  # B012
    # B013 <- L227-L227
    curr_date_ymd = (((mcyear * I_10000) + (mcmnth * I_100)) + mcday)
    # B014 <- L231-L231
    yr = _f_int_div(curr_date_ymd, I_10000)
    # B015 <- L232-L232
    mon = _f_int_div(_f_mod(curr_date_ymd, I_10000), I_100)
    # B016 <- L233-L233
    day = _f_mod(curr_date_ymd, I_100)
    return yr, mon, day, tod

def get_prev_date():
    """L238-L320 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    yr = 0
    mon = 0
    day = 0
    tod = 0
    nsecs = 0
    ndays = 0
    nyears = 0
    mcyear = 0
    mcmnth = 0
    mcday = 0
    days_per_month = 0
    date_ymd = 0
    # B001 <- L263-L263
    mcyear = _f_int_div(start_date_ymd, I_10000)
    # B002 <- L267-L267
    nsecs = (((itim - 1)) * dtstep)
    # B003 <- L268-L268
    ndays = _f_int_div(((nsecs + start_date_tod)), I_86400)
    # B004 <- L269-L273
    if isleap(mcyear, CALKINDFLAG):
        nyears = _f_int_div(ndays, I_366)
    else:
        nyears = _f_int_div(ndays, I_365)
    # B005 <- L278-L282
    if isleap(mcyear, CALKINDFLAG):
        ndays = _f_mod(ndays, I_366)
    else:
        ndays = _f_mod(ndays, I_365)
    # B006 <- L286-L286
    tod = _f_mod((nsecs + start_date_tod), I_86400)
    # B007 <- L290-L290
    mcyear = (_f_int_div(start_date_ymd, I_10000) + nyears)
    # B008 <- L291-L291
    mcmnth = _f_int_div(_f_mod(start_date_ymd, I_10000), I_100)
    # B009 <- L292-L292
    mcday = (_f_mod(start_date_ymd, I_100) + ndays)
    # B010 <- L297-L297
    pass  # continue
    # B011 <- L298-L302
    if isleap(mcyear, CALKINDFLAG):
        days_per_month = MDAYLEAP[mcmnth - 1]
    else:
        days_per_month = MDAY[mcmnth - 1]
    # B012 <- L303-L311 AGENT_QUEUE: goto 10 is not a loop-exit pattern
    raise NotImplementedError('goto 10 is not a loop-exit pattern')  # B012
    # B013 <- L312-L312
    date_ymd = (((mcyear * I_10000) + (mcmnth * I_100)) + mcday)
    # B014 <- L316-L316
    yr = _f_int_div(date_ymd, I_10000)
    # B015 <- L317-L317
    mon = _f_int_div(_f_mod(date_ymd, I_10000), I_100)
    # B016 <- L318-L318
    day = _f_mod(date_ymd, I_100)
    return yr, mon, day, tod

def get_curr_time():
    """L323-L342 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    days = 0
    seconds = 0
    nsecs = 0
    # B001 <- L338-L338
    nsecs = (itim * dtstep)
    # B002 <- L339-L339
    days = _f_int_div(((nsecs + start_date_tod)), I_86400)
    # B003 <- L340-L340
    seconds = _f_mod((nsecs + start_date_tod), I_86400)
    return days, seconds

def get_curr_calday(offset=None):
    """L345-L414 function (machine-translated)."""
    get_curr_calday = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    yr = 0
    mon = 0
    day = 0
    tod = 0
    calday = 0.0
    # B001 <- L364-L410
    if (offset < 0):
        calday = get_prev_calday()
    elif (offset > 0):
        pass  # write(iulog,...) log — no dataflow
        raise RuntimeError('endrun')  # endrun (infra stub)
    else:
        yr, mon, day, tod = get_curr_date()
        if isleap(yr, CALKINDFLAG):
            calday = ((np.float64(MDAYLEAPCUM[((mon - 1)) - (0)]) + np.float64(day)) + (np.float64(tod) / F_86400P))
        else:
            calday = ((np.float64(MDAYCUM[((mon - 1)) - (0)]) + np.float64(day)) + (np.float64(tod) / F_86400P))
        if ((((calday > F32_366P)) and ((calday <= F32_367P))) and ((_fstr_eq(_f_trim(CALKINDFLAG), 'GREGORIAN')))):
            calday = (calday - 1.0)
        if ((calday < 1.0) or (calday > F32_366P)):
            pass  # write(iulog,...) log — no dataflow
            raise RuntimeError('endrun')  # endrun (infra stub)
    # B002 <- L412-L412
    get_curr_calday = calday
    return get_curr_calday

def get_prev_calday():
    """L417-L464 function (machine-translated)."""
    get_prev_calday = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    yr = 0
    mon = 0
    day = 0
    tod = 0
    calday = 0.0
    # B001 <- L433-L433
    yr, mon, day, tod = get_prev_date()
    # B002 <- L437-L441
    if isleap(yr, CALKINDFLAG):
        calday = ((np.float64(MDAYLEAPCUM[((mon - 1)) - (0)]) + np.float64(day)) + (np.float64(tod) / F_86400P))
    else:
        calday = ((np.float64(MDAYCUM[((mon - 1)) - (0)]) + np.float64(day)) + (np.float64(tod) / F_86400P))
    # B003 <- L450-L452
    if ((((calday > F32_366P)) and ((calday <= F32_367P))) and ((_fstr_eq(_f_trim(CALKINDFLAG), 'GREGORIAN')))):
        calday = (calday - 1.0)
    # B004 <- L457-L460
    if ((calday < 1.0) or (calday > F32_366P)):
        pass  # write(iulog,...) log — no dataflow
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B005 <- L462-L462
    get_prev_calday = calday
    return get_prev_calday

def is_end_curr_day():
    """L467-L484 function (machine-translated)."""
    is_end_curr_day = False
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    yr = 0
    mon = 0
    day = 0
    tod = 0
    # B001 <- L481-L481
    yr, mon, day, tod = get_curr_date()
    # B002 <- L482-L482
    is_end_curr_day = ((tod == 0))
    return is_end_curr_day

def is_end_curr_month():
    """L487-L504 function (machine-translated)."""
    is_end_curr_month = False
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    yr = 0
    mon = 0
    day = 0
    tod = 0
    # B001 <- L501-L501
    yr, mon, day, tod = get_curr_date()
    # B002 <- L502-L502
    is_end_curr_month = (((day == 1) and (tod == 0)))
    return is_end_curr_month
