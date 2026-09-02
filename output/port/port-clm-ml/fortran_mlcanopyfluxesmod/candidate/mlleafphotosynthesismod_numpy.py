"""Machine-translated from MLLeafPhotosynthesisMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call ft before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
import re as _re
from typing import Any

import numpy as np

from mlleafphotosynthesismod_constants import *  # noqa: F401,F403
from mlleafphotosynthesismod_use_constants import *  # noqa: F401,F403
import mlcanopyfluxestype_numpy as _mlca
import mlclm_varcon_numpy as _mlc
import mlclm_varctl_numpy as _mlcl
import mlmathtoolsmod_numpy as _mlm
import mlpftconmod_numpy as _mlp
import mlwatervapormod_numpy as _mlw
import patchtype_numpy as _patchtype
import pftconmod_numpy as _pftconmod

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'ft': {'kind': 'function', 'args': [{'name': 'tl', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'ha', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'ans', 'result_dtype': 'float64'}, 'fth': {'kind': 'function', 'args': [{'name': 'tl', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'hd', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'se', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'c', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'ans', 'result_dtype': 'float64'}, 'fth25': {'kind': 'function', 'args': [{'name': 'hd', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'se', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'ans', 'result_dtype': 'float64'}, 'leafphotosynthesis': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'cifunc': {'kind': 'subroutine', 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'ci_val', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'ci_dif', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'cifuncgs': {'kind': 'subroutine', 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'ci_val', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'stomataoptimization': {'kind': 'subroutine', 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'stomataefficiency': {'kind': 'subroutine', 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'gs_val', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'check', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'realizedrate': {'kind': 'subroutine', 'args': [{'name': 'c3psn', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'ac', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'aj', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'ap', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'agross', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}}

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

def _make_patch_type():
    """factory for type(patch_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.column = None
    o.gridcell = None
    o.itype = None
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


def ft(tl, ha):
    """L34-L54 function (machine-translated)."""
    ans = 0.0
    # B001 <- L52-L52
    ans = math.exp(((ha / ((_mlc.rgas * ((TFRZ + F_25P))))) * ((1.0 - (((TFRZ + F_25P)) / tl)))))
    return ans

def fth(tl, hd, se, c):
    """L57-L78 function (machine-translated)."""
    ans = 0.0
    # B001 <- L76-L76
    ans = (c / ((1.0 + math.exp(((((-hd) + (se * tl))) / ((_mlc.rgas * tl)))))))
    return ans

def fth25(hd, se):
    """L81-L101 function (machine-translated)."""
    ans = 0.0
    # B001 <- L99-L99
    ans = (1.0 + math.exp(((((-hd) + (se * ((TFRZ + F_25P))))) / ((_mlc.rgas * ((TFRZ + F_25P)))))))
    return ans

def leafphotosynthesis(num_filter, filter, il, mlcanopy_inst):
    """L104-L465 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    tol = np.float64('0.1')
    fp = 0
    p = 0
    ic = 0
    vcmaxha = 0.0
    jmaxha = 0.0
    vcmaxhd = 0.0
    jmaxhd = 0.0
    vcmaxse = 0.0
    jmaxse = 0.0
    vcmaxc = 0.0
    jmaxc = 0.0
    rdc = 0.0
    qabs = 0.0
    desat = 0.0
    gs_err = 0.0
    an_err = 0.0
    aquad = 0.0
    bquad = 0.0
    cquad = 0.0
    r1 = 0.0
    r2 = 0.0
    ci0 = 0.0
    ci1 = 0.0
    hs_term = 0.0
    vpd_term = 0.0
    t1 = 0.0
    t2 = 0.0
    t3 = 0.0
    t4 = 0.0
    fpsi = 0.0
    # B001 <- L167-L464
    c3psn = _pftconmod.pftcon.c3psn
    g0_bb = _mlp.mlpftcon.g0_bb
    g1_bb = _mlp.mlpftcon.g1_bb
    g0_med = _mlp.mlpftcon.g0_med
    g1_med = _mlp.mlpftcon.g1_med
    psi50_gs = _mlp.mlpftcon.psi50_gs
    shape_gs = _mlp.mlpftcon.shape_gs
    gsmin_spa = _mlp.mlpftcon.gsmin_spa
    tacclim = mlcanopy_inst.tacclim_forcing
    ncan = mlcanopy_inst.ncan_canopy
    dpai = mlcanopy_inst.dpai_profile
    eair = mlcanopy_inst.eair_profile
    cair = mlcanopy_inst.cair_profile
    vcmax25 = mlcanopy_inst.vcmax25_leaf
    jmax25 = mlcanopy_inst.jmax25_leaf
    kp25 = mlcanopy_inst.kp25_leaf
    rd25 = mlcanopy_inst.rd25_leaf
    tleaf = mlcanopy_inst.tleaf_leaf
    gbv = mlcanopy_inst.gbv_leaf
    gbc = mlcanopy_inst.gbc_leaf
    apar = mlcanopy_inst.apar_leaf
    lwp = mlcanopy_inst.lwp_leaf
    g0 = mlcanopy_inst.g0_canopy
    g1 = mlcanopy_inst.g1_canopy
    btran = mlcanopy_inst.btran_soil
    kc = mlcanopy_inst.kc_leaf
    ko = mlcanopy_inst.ko_leaf
    cp = mlcanopy_inst.cp_leaf
    vcmax = mlcanopy_inst.vcmax_leaf
    jmax = mlcanopy_inst.jmax_leaf
    je = mlcanopy_inst.je_leaf
    kp = mlcanopy_inst.kp_leaf
    rd = mlcanopy_inst.rd_leaf
    ci = mlcanopy_inst.ci_leaf
    hs = mlcanopy_inst.hs_leaf
    vpd = mlcanopy_inst.vpd_leaf
    ceair = mlcanopy_inst.ceair_leaf
    leaf_esat = mlcanopy_inst.leaf_esat_leaf
    gspot = mlcanopy_inst.gspot_leaf
    ac = mlcanopy_inst.ac_leaf
    aj = mlcanopy_inst.aj_leaf
    ap = mlcanopy_inst.ap_leaf
    agross = mlcanopy_inst.agross_leaf
    anet = mlcanopy_inst.anet_leaf
    cs = mlcanopy_inst.cs_leaf
    gs = mlcanopy_inst.gs_leaf
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            if (_mlcl.acclim_type == 0):
                vcmaxha = _mlc.vcmaxha_noacclim
                jmaxha = _mlc.jmaxha_noacclim
                vcmaxhd = _mlc.vcmaxhd_noacclim
                jmaxhd = _mlc.jmaxhd_noacclim
                vcmaxse = _mlc.vcmaxse_noacclim
                jmaxse = _mlc.jmaxse_noacclim
            elif (_mlcl.acclim_type == 1):
                vcmaxha = _mlc.vcmaxha_acclim
                jmaxha = _mlc.jmaxha_acclim
                vcmaxhd = _mlc.vcmaxhd_acclim
                jmaxhd = _mlc.jmaxhd_acclim
                _mlc.vcmaxse_acclim = (F_668P39 - (F_1P07 * _f_min(_f_max(((tacclim[p - 1] - TFRZ)), F_11P), F_35P)))
                _mlc.jmaxse_acclim = (F_659P70 - (F_0P75 * _f_min(_f_max(((tacclim[p - 1] - TFRZ)), F_11P), F_35P)))
                vcmaxse = _mlc.vcmaxse_acclim
                jmaxse = _mlc.jmaxse_acclim
            else:
                raise RuntimeError('endrun')  # endrun (infra stub)
            vcmaxc = fth25(vcmaxhd, vcmaxse)
            jmaxc = fth25(jmaxhd, jmaxse)
            rdc = fth25(_mlc.rdhd, _mlc.rdse)
            if (dpai[p - 1, ic - 1] > 0.0):
                kc[p - 1, ic - 1, il - 1] = (_mlc.kc25 * ft(tleaf[p - 1, ic - 1, il - 1], _mlc.kcha))
                ko[p - 1, ic - 1, il - 1] = (_mlc.ko25 * ft(tleaf[p - 1, ic - 1, il - 1], _mlc.koha))
                cp[p - 1, ic - 1, il - 1] = (_mlc.cp25 * ft(tleaf[p - 1, ic - 1, il - 1], _mlc.cpha))
                vcmax[p - 1, ic - 1, il - 1] = ((vcmax25[p - 1, ic - 1, il - 1] * ft(tleaf[p - 1, ic - 1, il - 1], vcmaxha)) * fth(tleaf[p - 1, ic - 1, il - 1], vcmaxhd, vcmaxse, vcmaxc))
                jmax[p - 1, ic - 1, il - 1] = ((jmax25[p - 1, ic - 1, il - 1] * ft(tleaf[p - 1, ic - 1, il - 1], jmaxha)) * fth(tleaf[p - 1, ic - 1, il - 1], jmaxhd, jmaxse, jmaxc))
                rd[p - 1, ic - 1, il - 1] = ((rd25[p - 1, ic - 1, il - 1] * ft(tleaf[p - 1, ic - 1, il - 1], _mlc.rdha)) * fth(tleaf[p - 1, ic - 1, il - 1], _mlc.rdhd, _mlc.rdse, rdc))
                if (_f_nint(c3psn[(_patchtype.patch.itype[p - 1]) - (0)]) == 0):
                    t1 = (F32_2P0 ** ((((tleaf[p - 1, ic - 1, il - 1] - ((TFRZ + F_25P)))) / F_10P)))
                    t2 = (1.0 + math.exp((F_0P2 * ((((TFRZ + F_15P)) - tleaf[p - 1, ic - 1, il - 1])))))
                    t3 = (1.0 + math.exp((F_0P3 * ((tleaf[p - 1, ic - 1, il - 1] - ((TFRZ + F_40P)))))))
                    t4 = (1.0 + math.exp((F_1P3 * ((tleaf[p - 1, ic - 1, il - 1] - ((TFRZ + F_55P)))))))
                    vcmax[p - 1, ic - 1, il - 1] = ((vcmax25[p - 1, ic - 1, il - 1] * t1) / ((t2 * t3)))
                    rd[p - 1, ic - 1, il - 1] = ((rd25[p - 1, ic - 1, il - 1] * t1) / t4)
                    kp[p - 1, ic - 1, il - 1] = (kp25[p - 1, ic - 1, il - 1] * t1)
                btran[p - 1] = 1.0
                vcmax[p - 1, ic - 1, il - 1] = (vcmax[p - 1, ic - 1, il - 1] * btran[p - 1])
                if (_mlcl.gs_type == 0):
                    g0[p - 1] = g0_med[(_patchtype.patch.itype[p - 1]) - (0)]
                    g1[p - 1] = g1_med[(_patchtype.patch.itype[p - 1]) - (0)]
                elif (_mlcl.gs_type == 1):
                    g0[p - 1] = g0_bb[(_patchtype.patch.itype[p - 1]) - (0)]
                    g1[p - 1] = g1_bb[(_patchtype.patch.itype[p - 1]) - (0)]
                else:
                    g0[p - 1] = (-F_999P)
                    g1[p - 1] = (-F_999P)
                leaf_esat[p - 1, ic - 1, il - 1], desat = _mlw.satvap(tleaf[p - 1, ic - 1, il - 1])
                ceair[p - 1, ic - 1, il - 1] = _f_min(eair[p - 1, ic - 1], leaf_esat[p - 1, ic - 1, il - 1])
                if (_mlcl.gs_type == 1):
                    ceair[p - 1, ic - 1, il - 1] = _f_max(ceair[p - 1, ic - 1, il - 1], (_mlc.rh_min_bb * leaf_esat[p - 1, ic - 1, il - 1]))
                qabs = ((0.5 * _mlc.phi_psii) * apar[p - 1, ic - 1, il - 1])
                aquad = _mlc.theta_j
                bquad = (-((qabs + jmax[p - 1, ic - 1, il - 1])))
                cquad = (qabs * jmax[p - 1, ic - 1, il - 1])
                r1, r2 = _mlm.quadratic(aquad, bquad, cquad)
                je[p - 1, ic - 1, il - 1] = _f_min(r1, r2)
                if (_mlcl.gs_type == 0) or (_mlcl.gs_type == 1):
                    if (_f_nint(c3psn[(_patchtype.patch.itype[p - 1]) - (0)]) == 1):
                        ci0 = (F_0P7 * cair[p - 1, ic - 1])
                    elif (_f_nint(c3psn[(_patchtype.patch.itype[p - 1]) - (0)]) == 0):
                        ci0 = (F_0P4 * cair[p - 1, ic - 1])
                    ci1 = (ci0 * F_0P99)
                    ci[p - 1, ic - 1, il - 1] = _mlm.hybrid('LeafPhotosynthesis', p, ic, il, mlcanopy_inst, cifunc, ci0, ci1, tol)
                elif (_mlcl.gs_type == 2):
                    mlcanopy_inst = stomataoptimization(p, ic, il, mlcanopy_inst)
                else:
                    raise RuntimeError('endrun')  # endrun (infra stub)
                if (gs[p - 1, ic - 1, il - 1] < 0.0):
                    raise RuntimeError('endrun')  # endrun (infra stub)
                hs_term = ((((gbv[p - 1, ic - 1, il - 1] * ceair[p - 1, ic - 1, il - 1]) + (gs[p - 1, ic - 1, il - 1] * leaf_esat[p - 1, ic - 1, il - 1]))) / ((((gbv[p - 1, ic - 1, il - 1] + gs[p - 1, ic - 1, il - 1])) * leaf_esat[p - 1, ic - 1, il - 1])))
                vpd_term = (((leaf_esat[p - 1, ic - 1, il - 1] - (hs_term * leaf_esat[p - 1, ic - 1, il - 1]))) * F_0P001)
                if (_mlcl.gs_type == 1):
                    gs_err = (g0[p - 1] + (((g1[p - 1] * _f_max(anet[p - 1, ic - 1, il - 1], 0.0)) * hs_term) / cs[p - 1, ic - 1, il - 1]))
                    if (abs((gs[p - 1, ic - 1, il - 1] - gs_err)) > F_1PEM06):
                        raise RuntimeError('endrun')  # endrun (infra stub)
                elif (_mlcl.gs_type == 0):
                    if (((leaf_esat[p - 1, ic - 1, il - 1] - ceair[p - 1, ic - 1, il - 1])) > _mlc.vpd_min_med):
                        gs_err = (g0[p - 1] + (((_mlc.dh2o_to_dco2 * ((1.0 + (g1[p - 1] / math.sqrt(vpd_term))))) * _f_max(anet[p - 1, ic - 1, il - 1], 0.0)) / cs[p - 1, ic - 1, il - 1]))
                        if (abs((gs[p - 1, ic - 1, il - 1] - gs_err)) > F_1PEM06):
                            raise RuntimeError('endrun')  # endrun (infra stub)
                an_err = (((cair[p - 1, ic - 1] - ci[p - 1, ic - 1, il - 1])) / (((1.0 / gbc[p - 1, ic - 1, il - 1]) + (_mlc.dh2o_to_dco2 / gs[p - 1, ic - 1, il - 1]))))
                if ((anet[p - 1, ic - 1, il - 1] > 0.0) and (abs((anet[p - 1, ic - 1, il - 1] - an_err)) > F_0P01)):
                    raise RuntimeError('endrun')  # endrun (infra stub)
            else:
                rd[p - 1, ic - 1, il - 1] = 0.0
                if (_mlcl.gs_type == 0) or (_mlcl.gs_type == 1):
                    mlcanopy_inst, ci[p - 1, ic - 1, il - 1] = cifunc(p, ic, il, mlcanopy_inst, 0.0)
                elif (_mlcl.gs_type == 2):
                    mlcanopy_inst, ci[p - 1, ic - 1, il - 1] = cifuncgs(p, ic, il, mlcanopy_inst)
                else:
                    raise RuntimeError('endrun')  # endrun (infra stub)
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            gspot[p - 1, ic - 1, il - 1] = gs[p - 1, ic - 1, il - 1]
            if (dpai[p - 1, ic - 1] > 0.0):
                if (_mlcl.gspot_type == 0):
                    fpsi = 1.0
                elif (_mlcl.gspot_type == 1):
                    fpsi = (1.0 / ((1.0 + (((lwp[p - 1, ic - 1, il - 1] / psi50_gs[(_patchtype.patch.itype[p - 1]) - (0)])) ** shape_gs[(_patchtype.patch.itype[p - 1]) - (0)]))))
                gs[p - 1, ic - 1, il - 1] = _f_max((gspot[p - 1, ic - 1, il - 1] * fpsi), gsmin_spa[(_patchtype.patch.itype[p - 1]) - (0)])
                mlcanopy_inst, ci[p - 1, ic - 1, il - 1] = cifuncgs(p, ic, il, mlcanopy_inst)
                hs[p - 1, ic - 1, il - 1] = ((((gbv[p - 1, ic - 1, il - 1] * eair[p - 1, ic - 1]) + (gs[p - 1, ic - 1, il - 1] * leaf_esat[p - 1, ic - 1, il - 1]))) / ((((gbv[p - 1, ic - 1, il - 1] + gs[p - 1, ic - 1, il - 1])) * leaf_esat[p - 1, ic - 1, il - 1])))
                vpd[p - 1, ic - 1, il - 1] = _f_max((leaf_esat[p - 1, ic - 1, il - 1] - (hs[p - 1, ic - 1, il - 1] * leaf_esat[p - 1, ic - 1, il - 1])), F_0P1)
            else:
                hs[p - 1, ic - 1, il - 1] = 0.0
                vpd[p - 1, ic - 1, il - 1] = 0.0
    return mlcanopy_inst

def cifunc(p, ic, il, mlcanopy_inst, ci_val):
    """L468-L646 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    ci_dif = 0.0
    aquad = 0.0
    bquad = 0.0
    cquad = 0.0
    r1 = 0.0
    r2 = 0.0
    gleaf = 0.0
    cinew = 0.0
    term = 0.0
    vpd_term = 0.0
    # B001 <- L502-L645
    c3psn = _pftconmod.pftcon.c3psn
    o2ref = mlcanopy_inst.o2ref_forcing
    g0 = mlcanopy_inst.g0_canopy
    g1 = mlcanopy_inst.g1_canopy
    dpai = mlcanopy_inst.dpai_profile
    cair = mlcanopy_inst.cair_profile
    gbv = mlcanopy_inst.gbv_leaf
    gbc = mlcanopy_inst.gbc_leaf
    apar = mlcanopy_inst.apar_leaf
    kc = mlcanopy_inst.kc_leaf
    ko = mlcanopy_inst.ko_leaf
    cp = mlcanopy_inst.cp_leaf
    vcmax = mlcanopy_inst.vcmax_leaf
    je = mlcanopy_inst.je_leaf
    kp = mlcanopy_inst.kp_leaf
    rd = mlcanopy_inst.rd_leaf
    ceair = mlcanopy_inst.ceair_leaf
    leaf_esat = mlcanopy_inst.leaf_esat_leaf
    ac = mlcanopy_inst.ac_leaf
    aj = mlcanopy_inst.aj_leaf
    ap = mlcanopy_inst.ap_leaf
    agross = mlcanopy_inst.agross_leaf
    anet = mlcanopy_inst.anet_leaf
    cs = mlcanopy_inst.cs_leaf
    gs = mlcanopy_inst.gs_leaf
    if (dpai[p - 1, ic - 1] > 0.0):
        if (_f_nint(c3psn[(_patchtype.patch.itype[p - 1]) - (0)]) == 1):
            ac[p - 1, ic - 1, il - 1] = ((vcmax[p - 1, ic - 1, il - 1] * _f_max((ci_val - cp[p - 1, ic - 1, il - 1]), 0.0)) / ((ci_val + (kc[p - 1, ic - 1, il - 1] * ((1.0 + (o2ref[p - 1] / ko[p - 1, ic - 1, il - 1])))))))
            aj[p - 1, ic - 1, il - 1] = ((je[p - 1, ic - 1, il - 1] * _f_max((ci_val - cp[p - 1, ic - 1, il - 1]), 0.0)) / (((F_4P * ci_val) + (F_8P * cp[p - 1, ic - 1, il - 1]))))
            ap[p - 1, ic - 1, il - 1] = 0.0
        elif (_f_nint(c3psn[(_patchtype.patch.itype[p - 1]) - (0)]) == 0):
            ac[p - 1, ic - 1, il - 1] = vcmax[p - 1, ic - 1, il - 1]
            aj[p - 1, ic - 1, il - 1] = (_mlc.qe_c4 * apar[p - 1, ic - 1, il - 1])
            ap[p - 1, ic - 1, il - 1] = (kp[p - 1, ic - 1, il - 1] * _f_max(ci_val, 0.0))
        agross[p - 1, ic - 1, il - 1] = realizedrate(c3psn[(_patchtype.patch.itype[p - 1]) - (0)], ac[p - 1, ic - 1, il - 1], aj[p - 1, ic - 1, il - 1], ap[p - 1, ic - 1, il - 1])
        ac[p - 1, ic - 1, il - 1] = _f_max(ac[p - 1, ic - 1, il - 1], 0.0)
        aj[p - 1, ic - 1, il - 1] = _f_max(aj[p - 1, ic - 1, il - 1], 0.0)
        ap[p - 1, ic - 1, il - 1] = _f_max(ap[p - 1, ic - 1, il - 1], 0.0)
        agross[p - 1, ic - 1, il - 1] = _f_max(agross[p - 1, ic - 1, il - 1], 0.0)
        anet[p - 1, ic - 1, il - 1] = (agross[p - 1, ic - 1, il - 1] - rd[p - 1, ic - 1, il - 1])
        cs[p - 1, ic - 1, il - 1] = (cair[p - 1, ic - 1] - (anet[p - 1, ic - 1, il - 1] / gbc[p - 1, ic - 1, il - 1]))
        cs[p - 1, ic - 1, il - 1] = _f_max(cs[p - 1, ic - 1, il - 1], 1.0)
        if (_mlcl.gs_type == 1):
            if (anet[p - 1, ic - 1, il - 1] > 0.0):
                term = (anet[p - 1, ic - 1, il - 1] / cs[p - 1, ic - 1, il - 1])
                aquad = 1.0
                bquad = ((gbv[p - 1, ic - 1, il - 1] - g0[p - 1]) - (g1[p - 1] * term))
                cquad = (-(gbv[p - 1, ic - 1, il - 1] * ((g0[p - 1] + (((g1[p - 1] * term) * ceair[p - 1, ic - 1, il - 1]) / leaf_esat[p - 1, ic - 1, il - 1])))))
                r1, r2 = _mlm.quadratic(aquad, bquad, cquad)
                gs[p - 1, ic - 1, il - 1] = _f_max(r1, r2)
            else:
                gs[p - 1, ic - 1, il - 1] = g0[p - 1]
        elif (_mlcl.gs_type == 0):
            if (anet[p - 1, ic - 1, il - 1] > 0.0):
                vpd_term = (_f_max(((leaf_esat[p - 1, ic - 1, il - 1] - ceair[p - 1, ic - 1, il - 1])), _mlc.vpd_min_med) * F_0P001)
                term = ((_mlc.dh2o_to_dco2 * anet[p - 1, ic - 1, il - 1]) / cs[p - 1, ic - 1, il - 1])
                aquad = 1.0
                bquad = (-(((F_2P * ((g0[p - 1] + term))) + ((((g1[p - 1] * term)) * ((g1[p - 1] * term))) / ((gbv[p - 1, ic - 1, il - 1] * vpd_term))))))
                cquad = ((g0[p - 1] * g0[p - 1]) + ((((F_2P * g0[p - 1]) + (term * ((1.0 - ((g1[p - 1] * g1[p - 1]) / vpd_term)))))) * term))
                r1, r2 = _mlm.quadratic(aquad, bquad, cquad)
                gs[p - 1, ic - 1, il - 1] = _f_max(r1, r2)
            else:
                gs[p - 1, ic - 1, il - 1] = g0[p - 1]
        gleaf = (1.0 / (((1.0 / gbc[p - 1, ic - 1, il - 1]) + (_mlc.dh2o_to_dco2 / gs[p - 1, ic - 1, il - 1]))))
        cinew = (cair[p - 1, ic - 1] - (anet[p - 1, ic - 1, il - 1] / gleaf))
        ci_dif = (cinew - ci_val)
        if (anet[p - 1, ic - 1, il - 1] < 0.0):
            ci_dif = 0.0
    else:
        ac[p - 1, ic - 1, il - 1] = 0.0
        aj[p - 1, ic - 1, il - 1] = 0.0
        ap[p - 1, ic - 1, il - 1] = 0.0
        agross[p - 1, ic - 1, il - 1] = 0.0
        anet[p - 1, ic - 1, il - 1] = 0.0
        cs[p - 1, ic - 1, il - 1] = 0.0
        gs[p - 1, ic - 1, il - 1] = 0.0
        ci_dif = 0.0
    return mlcanopy_inst, ci_dif

def cifuncgs(p, ic, il, mlcanopy_inst):
    """L649-L789 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    ci_val = 0.0
    gleaf = 0.0
    a0 = 0.0
    b0 = 0.0
    aquad = 0.0
    bquad = 0.0
    cquad = 0.0
    r1 = 0.0
    r2 = 0.0
    # B001 <- L677-L788
    c3psn = _pftconmod.pftcon.c3psn
    o2ref = mlcanopy_inst.o2ref_forcing
    dpai = mlcanopy_inst.dpai_profile
    cair = mlcanopy_inst.cair_profile
    gbc = mlcanopy_inst.gbc_leaf
    gs = mlcanopy_inst.gs_leaf
    apar = mlcanopy_inst.apar_leaf
    kc = mlcanopy_inst.kc_leaf
    ko = mlcanopy_inst.ko_leaf
    cp = mlcanopy_inst.cp_leaf
    vcmax = mlcanopy_inst.vcmax_leaf
    je = mlcanopy_inst.je_leaf
    kp = mlcanopy_inst.kp_leaf
    rd = mlcanopy_inst.rd_leaf
    ac = mlcanopy_inst.ac_leaf
    aj = mlcanopy_inst.aj_leaf
    ap = mlcanopy_inst.ap_leaf
    agross = mlcanopy_inst.agross_leaf
    anet = mlcanopy_inst.anet_leaf
    cs = mlcanopy_inst.cs_leaf
    if (dpai[p - 1, ic - 1] > 0.0):
        gleaf = (1.0 / (((1.0 / gbc[p - 1, ic - 1, il - 1]) + (_mlc.dh2o_to_dco2 / gs[p - 1, ic - 1, il - 1]))))
        if (_f_nint(c3psn[(_patchtype.patch.itype[p - 1]) - (0)]) == 1):
            a0 = vcmax[p - 1, ic - 1, il - 1]
            b0 = (kc[p - 1, ic - 1, il - 1] * ((1.0 + (o2ref[p - 1] / ko[p - 1, ic - 1, il - 1]))))
            aquad = (1.0 / gleaf)
            bquad = ((-((cair[p - 1, ic - 1] + b0))) - (((a0 - rd[p - 1, ic - 1, il - 1])) / gleaf))
            cquad = ((a0 * ((cair[p - 1, ic - 1] - cp[p - 1, ic - 1, il - 1]))) - (rd[p - 1, ic - 1, il - 1] * ((cair[p - 1, ic - 1] + b0))))
            r1, r2 = _mlm.quadratic(aquad, bquad, cquad)
            ac[p - 1, ic - 1, il - 1] = (_f_min(r1, r2) + rd[p - 1, ic - 1, il - 1])
            a0 = (je[p - 1, ic - 1, il - 1] / F_4P)
            b0 = (F_2P * cp[p - 1, ic - 1, il - 1])
            aquad = (1.0 / gleaf)
            bquad = ((-((cair[p - 1, ic - 1] + b0))) - (((a0 - rd[p - 1, ic - 1, il - 1])) / gleaf))
            cquad = ((a0 * ((cair[p - 1, ic - 1] - cp[p - 1, ic - 1, il - 1]))) - (rd[p - 1, ic - 1, il - 1] * ((cair[p - 1, ic - 1] + b0))))
            r1, r2 = _mlm.quadratic(aquad, bquad, cquad)
            aj[p - 1, ic - 1, il - 1] = (_f_min(r1, r2) + rd[p - 1, ic - 1, il - 1])
            ap[p - 1, ic - 1, il - 1] = 0.0
        elif (_f_nint(c3psn[(_patchtype.patch.itype[p - 1]) - (0)]) == 0):
            ac[p - 1, ic - 1, il - 1] = vcmax[p - 1, ic - 1, il - 1]
            aj[p - 1, ic - 1, il - 1] = (_mlc.qe_c4 * apar[p - 1, ic - 1, il - 1])
            ap[p - 1, ic - 1, il - 1] = ((kp[p - 1, ic - 1, il - 1] * (((cair[p - 1, ic - 1] * gleaf) + rd[p - 1, ic - 1, il - 1]))) / ((gleaf + kp[p - 1, ic - 1, il - 1])))
        agross[p - 1, ic - 1, il - 1] = realizedrate(c3psn[(_patchtype.patch.itype[p - 1]) - (0)], ac[p - 1, ic - 1, il - 1], aj[p - 1, ic - 1, il - 1], ap[p - 1, ic - 1, il - 1])
        anet[p - 1, ic - 1, il - 1] = (agross[p - 1, ic - 1, il - 1] - rd[p - 1, ic - 1, il - 1])
        cs[p - 1, ic - 1, il - 1] = (cair[p - 1, ic - 1] - (anet[p - 1, ic - 1, il - 1] / gbc[p - 1, ic - 1, il - 1]))
        cs[p - 1, ic - 1, il - 1] = _f_max(cs[p - 1, ic - 1, il - 1], 1.0)
        ci_val = (cair[p - 1, ic - 1] - (anet[p - 1, ic - 1, il - 1] / gleaf))
    else:
        ac[p - 1, ic - 1, il - 1] = 0.0
        aj[p - 1, ic - 1, il - 1] = 0.0
        ap[p - 1, ic - 1, il - 1] = 0.0
        agross[p - 1, ic - 1, il - 1] = 0.0
        anet[p - 1, ic - 1, il - 1] = 0.0
        cs[p - 1, ic - 1, il - 1] = 0.0
        ci_val = 0.0
    return mlcanopy_inst, ci_val

def stomataoptimization(p, ic, il, mlcanopy_inst):
    """L792-L870 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    tol = np.float64('0.001')
    gs1 = 0.0
    gs2 = 0.0
    check1 = 0.0
    check2 = 0.0
    # B001 <- L817-L869
    gsmin_spa = _mlp.mlpftcon.gsmin_spa
    dpai = mlcanopy_inst.dpai_profile
    ci = mlcanopy_inst.ci_leaf
    gs = mlcanopy_inst.gs_leaf
    gs1 = gsmin_spa[(_patchtype.patch.itype[p - 1]) - (0)]
    gs2 = F_2P
    if (dpai[p - 1, ic - 1] > 0.0):
        mlcanopy_inst, check1 = stomataefficiency(p, ic, il, mlcanopy_inst, gs1)
        mlcanopy_inst, check2 = stomataefficiency(p, ic, il, mlcanopy_inst, gs2)
        if ((check1 * check2) < 0.0):
            if (_mlcl.gs_solver == 1):
                gs[p - 1, ic - 1, il - 1] = _mlm.zbrent('StomataOptimization', p, ic, il, mlcanopy_inst, stomataefficiency, gs1, gs2, tol)
            elif (_mlcl.gs_solver == 2):
                gs[p - 1, ic - 1, il - 1] = _mlm.bisection('StomataOptimization', p, ic, il, mlcanopy_inst, stomataefficiency, gs1, gs2, tol)
        else:
            gs[p - 1, ic - 1, il - 1] = gsmin_spa[(_patchtype.patch.itype[p - 1]) - (0)]
    else:
        gs[p - 1, ic - 1, il - 1] = 0.0
    mlcanopy_inst, ci[p - 1, ic - 1, il - 1] = cifuncgs(p, ic, il, mlcanopy_inst)
    return mlcanopy_inst

def stomataefficiency(p, ic, il, mlcanopy_inst, gs_val):
    """L873-L946 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    check = 0.0
    delta = 0.0
    an_low = 0.0
    an_high = 0.0
    hs = 0.0
    vpd = 0.0
    # B001 <- L906-L945
    iota_spa = _mlp.mlpftcon.iota_spa
    pref = mlcanopy_inst.pref_forcing
    eair = mlcanopy_inst.eair_profile
    gbv = mlcanopy_inst.gbv_leaf
    leaf_esat = mlcanopy_inst.leaf_esat_leaf
    gs = mlcanopy_inst.gs_leaf
    ci = mlcanopy_inst.ci_leaf
    anet = mlcanopy_inst.anet_leaf
    delta = F_0P001
    gs[p - 1, ic - 1, il - 1] = (gs_val - delta)
    mlcanopy_inst, ci[p - 1, ic - 1, il - 1] = cifuncgs(p, ic, il, mlcanopy_inst)
    an_low = anet[p - 1, ic - 1, il - 1]
    gs[p - 1, ic - 1, il - 1] = gs_val
    mlcanopy_inst, ci[p - 1, ic - 1, il - 1] = cifuncgs(p, ic, il, mlcanopy_inst)
    an_high = anet[p - 1, ic - 1, il - 1]
    hs = ((((gbv[p - 1, ic - 1, il - 1] * eair[p - 1, ic - 1]) + (gs[p - 1, ic - 1, il - 1] * leaf_esat[p - 1, ic - 1, il - 1]))) / ((((gbv[p - 1, ic - 1, il - 1] + gs[p - 1, ic - 1, il - 1])) * leaf_esat[p - 1, ic - 1, il - 1])))
    vpd = _f_max(((leaf_esat[p - 1, ic - 1, il - 1] - (hs * leaf_esat[p - 1, ic - 1, il - 1]))), _mlc.vpd_min_med)
    check = (((an_high - an_low)) - ((iota_spa[(_patchtype.patch.itype[p - 1]) - (0)] * delta) * ((vpd / pref[p - 1]))))
    return mlcanopy_inst, check

def realizedrate(c3psn, ac, aj, ap):
    """L949-L1024 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    agross = 0.0
    aquad = 0.0
    bquad = 0.0
    cquad = 0.0
    r1 = 0.0
    r2 = 0.0
    ai = 0.0
    # B001 <- L973-L1022
    if (_mlcl.colim_type == 0):
        if (_f_nint(c3psn) == 1):
            agross = _f_min(ac, aj)
        elif (_f_nint(c3psn) == 0):
            agross = _f_min(ac, aj, ap)
    elif (_mlcl.colim_type == 1):
        if (_f_nint(c3psn) == 1):
            aquad = _mlc.colim_c3a
        elif (_f_nint(c3psn) == 0):
            aquad = _mlc.colim_c4a
        bquad = (-((ac + aj)))
        cquad = (ac * aj)
        r1, r2 = _mlm.quadratic(aquad, bquad, cquad)
        ai = _f_min(r1, r2)
        if (_f_nint(c3psn) == 1):
            agross = ai
        elif (_f_nint(c3psn) == 0):
            aquad = _mlc.colim_c4b
            bquad = (-((ai + ap)))
            cquad = (ai * ap)
            r1, r2 = _mlm.quadratic(aquad, bquad, cquad)
            agross = _f_min(r1, r2)
    else:
        raise RuntimeError('endrun')  # endrun (infra stub)
    return agross


# Flattened adapters for the differential gate (recast.transform.numpy.flat).
class _Record:
    def __init__(self, **fields):
        self.__dict__.update(fields)

def leafphotosynthesis_flat(num_filter, filter, il, np_, mlcanopy_inst__ac_leaf, mlcanopy_inst__agross_leaf, mlcanopy_inst__aj_leaf, mlcanopy_inst__anet_leaf, mlcanopy_inst__ap_leaf, mlcanopy_inst__apar_leaf, mlcanopy_inst__btran_soil, mlcanopy_inst__cair_profile, mlcanopy_inst__ceair_leaf, mlcanopy_inst__ci_leaf, mlcanopy_inst__cp_leaf, mlcanopy_inst__cs_leaf, mlcanopy_inst__dpai_profile, mlcanopy_inst__eair_profile, mlcanopy_inst__g0_canopy, mlcanopy_inst__g1_canopy, mlcanopy_inst__gbc_leaf, mlcanopy_inst__gbv_leaf, mlcanopy_inst__gs_leaf, mlcanopy_inst__gspot_leaf, mlcanopy_inst__hs_leaf, mlcanopy_inst__je_leaf, mlcanopy_inst__jmax25_leaf, mlcanopy_inst__jmax_leaf, mlcanopy_inst__kc_leaf, mlcanopy_inst__ko_leaf, mlcanopy_inst__kp25_leaf, mlcanopy_inst__kp_leaf, mlcanopy_inst__leaf_esat_leaf, mlcanopy_inst__lwp_leaf, mlcanopy_inst__ncan_canopy, mlcanopy_inst__o2ref_forcing, mlcanopy_inst__pref_forcing, mlcanopy_inst__rd25_leaf, mlcanopy_inst__rd_leaf, mlcanopy_inst__tacclim_forcing, mlcanopy_inst__tleaf_leaf, mlcanopy_inst__vcmax25_leaf, mlcanopy_inst__vcmax_leaf, mlcanopy_inst__vpd_leaf, mlpftcon__g0_bb, mlpftcon__g0_med, mlpftcon__g1_bb, mlpftcon__g1_med, mlpftcon__gsmin_spa, mlpftcon__iota_spa, mlpftcon__psi50_gs, mlpftcon__shape_gs, patch__itype, pftcon__c3psn, mlclm_varcon__colim_c3a, mlclm_varcon__colim_c4a, mlclm_varcon__colim_c4b, mlclm_varcon__cp25, mlclm_varcon__cpha, mlclm_varcon__dh2o_to_dco2, mlclm_varcon__jmaxha_acclim, mlclm_varcon__jmaxha_noacclim, mlclm_varcon__jmaxhd_acclim, mlclm_varcon__jmaxhd_noacclim, mlclm_varcon__jmaxse_acclim, mlclm_varcon__jmaxse_noacclim, mlclm_varcon__kc25, mlclm_varcon__kcha, mlclm_varcon__ko25, mlclm_varcon__koha, mlclm_varcon__phi_psii, mlclm_varcon__qe_c4, mlclm_varcon__rdha, mlclm_varcon__rdhd, mlclm_varcon__rdse, mlclm_varcon__rgas, mlclm_varcon__rh_min_bb, mlclm_varcon__theta_j, mlclm_varcon__vcmaxha_acclim, mlclm_varcon__vcmaxha_noacclim, mlclm_varcon__vcmaxhd_acclim, mlclm_varcon__vcmaxhd_noacclim, mlclm_varcon__vcmaxse_acclim, mlclm_varcon__vcmaxse_noacclim, mlclm_varcon__vpd_min_med, mlclm_varctl__acclim_type, mlclm_varctl__colim_type, mlclm_varctl__gs_solver, mlclm_varctl__gs_type, mlclm_varctl__gspot_type):
    mlcanopy_inst = _Record(ac_leaf=mlcanopy_inst__ac_leaf, agross_leaf=mlcanopy_inst__agross_leaf, aj_leaf=mlcanopy_inst__aj_leaf, anet_leaf=mlcanopy_inst__anet_leaf, ap_leaf=mlcanopy_inst__ap_leaf, apar_leaf=mlcanopy_inst__apar_leaf, btran_soil=mlcanopy_inst__btran_soil, cair_profile=mlcanopy_inst__cair_profile, ceair_leaf=mlcanopy_inst__ceair_leaf, ci_leaf=mlcanopy_inst__ci_leaf, cp_leaf=mlcanopy_inst__cp_leaf, cs_leaf=mlcanopy_inst__cs_leaf, dpai_profile=mlcanopy_inst__dpai_profile, eair_profile=mlcanopy_inst__eair_profile, g0_canopy=mlcanopy_inst__g0_canopy, g1_canopy=mlcanopy_inst__g1_canopy, gbc_leaf=mlcanopy_inst__gbc_leaf, gbv_leaf=mlcanopy_inst__gbv_leaf, gs_leaf=mlcanopy_inst__gs_leaf, gspot_leaf=mlcanopy_inst__gspot_leaf, hs_leaf=mlcanopy_inst__hs_leaf, je_leaf=mlcanopy_inst__je_leaf, jmax25_leaf=mlcanopy_inst__jmax25_leaf, jmax_leaf=mlcanopy_inst__jmax_leaf, kc_leaf=mlcanopy_inst__kc_leaf, ko_leaf=mlcanopy_inst__ko_leaf, kp25_leaf=mlcanopy_inst__kp25_leaf, kp_leaf=mlcanopy_inst__kp_leaf, leaf_esat_leaf=mlcanopy_inst__leaf_esat_leaf, lwp_leaf=mlcanopy_inst__lwp_leaf, ncan_canopy=mlcanopy_inst__ncan_canopy, o2ref_forcing=mlcanopy_inst__o2ref_forcing, pref_forcing=mlcanopy_inst__pref_forcing, rd25_leaf=mlcanopy_inst__rd25_leaf, rd_leaf=mlcanopy_inst__rd_leaf, tacclim_forcing=mlcanopy_inst__tacclim_forcing, tleaf_leaf=mlcanopy_inst__tleaf_leaf, vcmax25_leaf=mlcanopy_inst__vcmax25_leaf, vcmax_leaf=mlcanopy_inst__vcmax_leaf, vpd_leaf=mlcanopy_inst__vpd_leaf)
    import mlpftconmod_numpy as _mlpftconmod
    if not hasattr(getattr(_mlpftconmod, 'mlpftcon', None), '__dict__'):
        _mlpftconmod.mlpftcon = _Record()
    _mlpftconmod.mlpftcon.g0_bb = mlpftcon__g0_bb
    _mlpftconmod.mlpftcon.g0_med = mlpftcon__g0_med
    _mlpftconmod.mlpftcon.g1_bb = mlpftcon__g1_bb
    _mlpftconmod.mlpftcon.g1_med = mlpftcon__g1_med
    _mlpftconmod.mlpftcon.gsmin_spa = mlpftcon__gsmin_spa
    _mlpftconmod.mlpftcon.iota_spa = mlpftcon__iota_spa
    _mlpftconmod.mlpftcon.psi50_gs = mlpftcon__psi50_gs
    _mlpftconmod.mlpftcon.shape_gs = mlpftcon__shape_gs
    import patchtype_numpy as _patchtype
    if not hasattr(getattr(_patchtype, 'patch', None), '__dict__'):
        _patchtype.patch = _Record()
    _patchtype.patch.itype = patch__itype
    import pftconmod_numpy as _pftconmod
    if not hasattr(getattr(_pftconmod, 'pftcon', None), '__dict__'):
        _pftconmod.pftcon = _Record()
    _pftconmod.pftcon.c3psn = pftcon__c3psn
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.colim_c3a = mlclm_varcon__colim_c3a
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.colim_c4a = mlclm_varcon__colim_c4a
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.colim_c4b = mlclm_varcon__colim_c4b
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cp25 = mlclm_varcon__cp25
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cpha = mlclm_varcon__cpha
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dh2o_to_dco2 = mlclm_varcon__dh2o_to_dco2
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmaxha_acclim = mlclm_varcon__jmaxha_acclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmaxha_noacclim = mlclm_varcon__jmaxha_noacclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmaxhd_acclim = mlclm_varcon__jmaxhd_acclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmaxhd_noacclim = mlclm_varcon__jmaxhd_noacclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmaxse_acclim = mlclm_varcon__jmaxse_acclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmaxse_noacclim = mlclm_varcon__jmaxse_noacclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.kc25 = mlclm_varcon__kc25
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.kcha = mlclm_varcon__kcha
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.ko25 = mlclm_varcon__ko25
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.koha = mlclm_varcon__koha
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.phi_psii = mlclm_varcon__phi_psii
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.qe_c4 = mlclm_varcon__qe_c4
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.rdha = mlclm_varcon__rdha
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.rdhd = mlclm_varcon__rdhd
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.rdse = mlclm_varcon__rdse
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.rgas = mlclm_varcon__rgas
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.rh_min_bb = mlclm_varcon__rh_min_bb
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.theta_j = mlclm_varcon__theta_j
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vcmaxha_acclim = mlclm_varcon__vcmaxha_acclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vcmaxha_noacclim = mlclm_varcon__vcmaxha_noacclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vcmaxhd_acclim = mlclm_varcon__vcmaxhd_acclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vcmaxhd_noacclim = mlclm_varcon__vcmaxhd_noacclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vcmaxse_acclim = mlclm_varcon__vcmaxse_acclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vcmaxse_noacclim = mlclm_varcon__vcmaxse_noacclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vpd_min_med = mlclm_varcon__vpd_min_med
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.acclim_type = mlclm_varctl__acclim_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.colim_type = mlclm_varctl__colim_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.gs_solver = mlclm_varctl__gs_solver
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.gs_type = mlclm_varctl__gs_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.gspot_type = mlclm_varctl__gspot_type
    _out = leafphotosynthesis(num_filter=num_filter, filter=filter, il=il, mlcanopy_inst=mlcanopy_inst)
    _out = (_out,)
    mlcanopy_inst_, = _out
    mlcanopy_inst__ac_leaf = mlcanopy_inst.ac_leaf
    mlcanopy_inst__agross_leaf = mlcanopy_inst.agross_leaf
    mlcanopy_inst__aj_leaf = mlcanopy_inst.aj_leaf
    mlcanopy_inst__anet_leaf = mlcanopy_inst.anet_leaf
    mlcanopy_inst__ap_leaf = mlcanopy_inst.ap_leaf
    mlcanopy_inst__btran_soil = mlcanopy_inst.btran_soil
    mlcanopy_inst__ceair_leaf = mlcanopy_inst.ceair_leaf
    mlcanopy_inst__ci_leaf = mlcanopy_inst.ci_leaf
    mlcanopy_inst__cp_leaf = mlcanopy_inst.cp_leaf
    mlcanopy_inst__cs_leaf = mlcanopy_inst.cs_leaf
    mlcanopy_inst__g0_canopy = mlcanopy_inst.g0_canopy
    mlcanopy_inst__g1_canopy = mlcanopy_inst.g1_canopy
    mlcanopy_inst__gs_leaf = mlcanopy_inst.gs_leaf
    mlcanopy_inst__gspot_leaf = mlcanopy_inst.gspot_leaf
    mlcanopy_inst__hs_leaf = mlcanopy_inst.hs_leaf
    mlcanopy_inst__je_leaf = mlcanopy_inst.je_leaf
    mlcanopy_inst__jmax_leaf = mlcanopy_inst.jmax_leaf
    mlcanopy_inst__kc_leaf = mlcanopy_inst.kc_leaf
    mlcanopy_inst__ko_leaf = mlcanopy_inst.ko_leaf
    mlcanopy_inst__kp_leaf = mlcanopy_inst.kp_leaf
    mlcanopy_inst__leaf_esat_leaf = mlcanopy_inst.leaf_esat_leaf
    mlcanopy_inst__rd_leaf = mlcanopy_inst.rd_leaf
    mlcanopy_inst__vcmax_leaf = mlcanopy_inst.vcmax_leaf
    mlcanopy_inst__vpd_leaf = mlcanopy_inst.vpd_leaf
    mlclm_varcon__jmaxse_acclim = _mlclm_varcon.jmaxse_acclim
    mlclm_varcon__vcmaxse_acclim = _mlclm_varcon.vcmaxse_acclim
    return mlcanopy_inst__ac_leaf, mlcanopy_inst__agross_leaf, mlcanopy_inst__aj_leaf, mlcanopy_inst__anet_leaf, mlcanopy_inst__ap_leaf, mlcanopy_inst__btran_soil, mlcanopy_inst__ceair_leaf, mlcanopy_inst__ci_leaf, mlcanopy_inst__cp_leaf, mlcanopy_inst__cs_leaf, mlcanopy_inst__g0_canopy, mlcanopy_inst__g1_canopy, mlcanopy_inst__gs_leaf, mlcanopy_inst__gspot_leaf, mlcanopy_inst__hs_leaf, mlcanopy_inst__je_leaf, mlcanopy_inst__jmax_leaf, mlcanopy_inst__kc_leaf, mlcanopy_inst__ko_leaf, mlcanopy_inst__kp_leaf, mlcanopy_inst__leaf_esat_leaf, mlcanopy_inst__rd_leaf, mlcanopy_inst__vcmax_leaf, mlcanopy_inst__vpd_leaf, mlclm_varcon__jmaxse_acclim, mlclm_varcon__vcmaxse_acclim

_SIGNATURES.update({
    'leafphotosynthesis_flat': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'num_filter'}]}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'np_', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlcanopy_inst__ac_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__agross_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__aj_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__anet_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ap_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__apar_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__btran_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__cair_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__ceair_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ci_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__cp_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__cs_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__dpai_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__eair_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__g0_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__g1_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gbc_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gbv_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gs_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gspot_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__hs_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__je_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__jmax25_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__jmax_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__kc_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ko_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__kp25_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__kp_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__leaf_esat_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lwp_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ncan_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__o2ref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__pref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rd25_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__rd_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__tacclim_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tleaf_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__vcmax25_leaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__vcmax_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__vpd_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlpftcon__g0_bb', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__g0_med', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__g1_bb', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__g1_med', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__gsmin_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__iota_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__psi50_gs', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__shape_gs', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'patch__itype', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'pftcon__c3psn', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlclm_varcon__colim_c3a', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__colim_c4a', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__colim_c4b', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cp25', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cpha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__dh2o_to_dco2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxha_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxha_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxhd_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxhd_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxse_acclim', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxse_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__kc25', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__kcha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__ko25', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__koha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__phi_psii', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__qe_c4', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rdha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rdhd', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rdse', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rgas', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rh_min_bb', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__theta_j', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxha_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxha_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxhd_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxhd_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxse_acclim', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxse_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vpd_min_med', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__acclim_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__colim_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__gs_solver', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__gs_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__gspot_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}], 'result': None, 'result_dtype': None},
})
