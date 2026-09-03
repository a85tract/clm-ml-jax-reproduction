"""Machine-translated from MLMathToolsMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call hybrid before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
import re as _re
from typing import Any

import numpy as np

from mlmathtoolsmod_constants import *  # noqa: F401,F403
from mlmathtoolsmod_use_constants import *  # noqa: F401,F403
import mlcanopyfluxestype_numpy as _mlc

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'hybrid': {'kind': 'function', 'public': True, 'args': [{'name': 'msg', 'dtype': 'str', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'func', 'dtype': 'PROCEDURE', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'xa', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'xb', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'tol', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'root', 'result_dtype': 'float64'}, 'zbrent': {'kind': 'function', 'public': True, 'args': [{'name': 'msg', 'dtype': 'str', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'func', 'dtype': 'PROCEDURE', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'xa', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'xb', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'tol', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'root', 'result_dtype': 'float64'}, 'bisection': {'kind': 'function', 'public': True, 'args': [{'name': 'msg', 'dtype': 'str', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'func', 'dtype': 'PROCEDURE', 'intent': 'UNKNOWN', 'optional': False}, {'name': 'xa', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'xb', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'tol', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'root', 'result_dtype': 'float64'}, 'quadratic': {'kind': 'subroutine', 'public': True, 'args': [{'name': 'a', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'b', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'c', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'r1', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}, {'name': 'r2', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'tridiag': {'kind': 'subroutine', 'public': True, 'args': [{'name': 'a', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'n'}]}, {'name': 'b', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'n'}]}, {'name': 'c', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'n'}]}, {'name': 'r', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'n'}]}, {'name': 'u', 'dtype': 'float64', 'intent': 'OUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'n'}], 'buffer': True}, {'name': 'n', 'dtype': 'int32', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'tridiag_2eq': {'kind': 'subroutine', 'public': True, 'args': [{'name': 'a1', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'b11', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'b12', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'c1', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'd1', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'a2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'b21', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'b22', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'c2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'd2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 't', 'dtype': 'float64', 'intent': 'OUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}], 'buffer': True}, {'name': 'q', 'dtype': 'float64', 'intent': 'OUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nlevmlcan'}], 'buffer': True}, {'name': 'n', 'dtype': 'int32', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'log_gamma_function': {'kind': 'function', 'public': True, 'args': [{'name': 'x', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'gammaln', 'result_dtype': 'float64'}, 'beta_function': {'kind': 'function', 'public': True, 'args': [{'name': 'a', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'b', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'beta', 'result_dtype': 'float64'}, 'beta_distribution_pdf': {'kind': 'function', 'public': True, 'args': [{'name': 'a', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'b', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'x', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'beta_pdf', 'result_dtype': 'float64'}, 'beta_distribution_cdf': {'kind': 'function', 'public': True, 'args': [{'name': 'a', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'b', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'x', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'beta_cdf', 'result_dtype': 'float64'}, 'beta_function_incomplete_cf': {'kind': 'function', 'public': False, 'args': [{'name': 'a', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'b', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'x', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'betacf', 'result_dtype': 'float64'}}

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


def hybrid(msg, p, ic, il, mlcanopy_inst, func, xa, xb, tol):
    """L46-L140 function (machine-translated)."""
    root = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    itmax = 40
    x0 = 0.0
    x1 = 0.0
    f0 = 0.0
    f1 = 0.0
    minx = 0.0
    minf = 0.0
    dx = 0.0
    x = 0.0
    iter = 0
    # B001 <- L78-L78
    x0 = xa
    # B002 <- L79-L79
    mlcanopy_inst, f0 = func(p, ic, il, mlcanopy_inst, x0)
    # B003 <- L80-L83
    if (f0 == 0.0):
        root = x0
        return root
    # B004 <- L85-L85
    x1 = xb
    # B005 <- L86-L86
    mlcanopy_inst, f1 = func(p, ic, il, mlcanopy_inst, x1)
    # B006 <- L87-L90
    if (f1 == 0.0):
        root = x1
        return root
    # B007 <- L92-L98
    if (f1 < f0):
        minx = x1
        minf = f1
    else:
        minx = x0
        minf = f0
    # B008 <- L102-L102
    iter = 0
    # B009 <- L103-L136
    while True:
        iter = (iter + 1)
        dx = (-((f1 * ((x1 - x0))) / ((f1 - f0))))
        x = (x1 + dx)
        if (abs(dx) < tol):
            x0 = x
            break
        x0 = x1
        f0 = f1
        x1 = x
        mlcanopy_inst, f1 = func(p, ic, il, mlcanopy_inst, x1)
        if (f1 < minf):
            minx = x1
            minf = f1
        if ((f1 * f0) < 0.0):
            x = zbrent(msg, p, ic, il, mlcanopy_inst, func, x0, x1, tol)
            x0 = x
            break
        if (iter > itmax):
            mlcanopy_inst, f1 = func(p, ic, il, mlcanopy_inst, minx)
            x0 = minx
            break
    # B010 <- L138-L138
    root = x0
    return root

def zbrent(msg, p, ic, il, mlcanopy_inst, func, xa, xb, tol):
    """L143-L248 function (machine-translated)."""
    root = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    itmax = 50
    eps = np.float64('1.E-08')
    iter = 0
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0
    e = 0.0
    fa = 0.0
    fb = 0.0
    fc = 0.0
    pp = 0.0
    q = 0.0
    r = 0.0
    s = 0.0
    tol1 = 0.0
    xm = 0.0
    # B001 <- L171-L171
    a = xa
    # B002 <- L172-L172
    b = xb
    # B003 <- L173-L173
    mlcanopy_inst, fa = func(p, ic, il, mlcanopy_inst, a)
    # B004 <- L174-L174
    mlcanopy_inst, fb = func(p, ic, il, mlcanopy_inst, b)
    # B005 <- L176-L182
    if ((((fa > 0.0) and (fb > 0.0))) or (((fa < 0.0) and (fb < 0.0)))):
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B006 <- L183-L183
    c = b
    # B007 <- L184-L184
    fc = fb
    # B008 <- L185-L185
    iter = 0
    # B009 <- L186-L239
    while True:
        if (iter == itmax):
            break
        iter = (iter + 1)
        if ((((fb > 0.0) and (fc > 0.0))) or (((fb < 0.0) and (fc < 0.0)))):
            c = a
            fc = fa
            d = (b - a)
            e = d
        if (abs(fc) < abs(fb)):
            a = b
            b = c
            c = a
            fa = fb
            fb = fc
            fc = fa
        tol1 = (((F_2P * eps) * abs(b)) + (0.5 * tol))
        xm = (0.5 * ((c - b)))
        if ((abs(xm) <= tol1) or (fb == 0.0)):
            break
        if ((abs(e) >= tol1) and (abs(fa) > abs(fb))):
            s = (fb / fa)
            if (a == c):
                pp = ((F_2P * xm) * s)
                q = (1.0 - s)
            else:
                q = (fa / fc)
                r = (fb / fc)
                pp = (s * (((((F_2P * xm) * q) * ((q - r))) - (((b - a)) * ((r - 1.0))))))
                q = ((((q - 1.0)) * ((r - 1.0))) * ((s - 1.0)))
            if (pp > 0.0):
                q = (-q)
            pp = abs(pp)
            if ((F_2P * pp) < _f_min((((F_3P * xm) * q) - abs((tol1 * q))), abs((e * q)))):
                e = d
                d = (pp / q)
            else:
                d = xm
                e = d
        else:
            d = xm
            e = d
        a = b
        fa = fb
        if (abs(d) > tol1):
            b = (b + d)
        else:
            b = (b + _f_sign(tol1, xm))
        mlcanopy_inst, fb = func(p, ic, il, mlcanopy_inst, b)
        if (fb == 0.0):
            break
    # B010 <- L240-L240
    root = b
    # B011 <- L242-L246
    if (iter == itmax):
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        raise RuntimeError('endrun')  # endrun (infra stub)
    return root

def bisection(msg, p, ic, il, mlcanopy_inst, func, xa, xb, tol):
    """L251-L311 function (machine-translated)."""
    root = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    itmax = 100
    iter = 0
    a = 0.0
    b = 0.0
    c = 0.0
    fa = 0.0
    fb = 0.0
    fc = 0.0
    # B001 <- L278-L278
    a = xa
    # B002 <- L279-L279
    b = xb
    # B003 <- L280-L280
    mlcanopy_inst, fa = func(p, ic, il, mlcanopy_inst, a)
    # B004 <- L281-L281
    mlcanopy_inst, fb = func(p, ic, il, mlcanopy_inst, b)
    # B005 <- L283-L289
    if ((fa * fb) > 0.0):
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B006 <- L291-L291
    iter = 1
    # B007 <- L292-L301
    while ((abs((b - a)) > tol) and (iter <= itmax)):
        c = (((a + b)) / F_2P)
        mlcanopy_inst, fc = func(p, ic, il, mlcanopy_inst, c)
        if ((fa * fc) < 0.0):
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        iter = (iter + 1)
    # B008 <- L303-L307
    if (iter > itmax):
        pass  # write(iulog,...) log — no dataflow
        pass  # write(iulog,...) log — no dataflow
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B009 <- L309-L309
    root = c
    return root

def quadratic(a, b, c):
    """L314-L348 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    r1 = 0.0
    r2 = 0.0
    q = 0.0
    # B001 <- L330-L333
    if (a == 0.0):
        pass  # write(iulog,...) log — no dataflow
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B002 <- L335-L339
    if (b >= 0.0):
        q = (-(0.5 * ((b + math.sqrt(((b * b) - ((F_4P * a) * c)))))))
    else:
        q = (-(0.5 * ((b - math.sqrt(((b * b) - ((F_4P * a) * c)))))))
    # B003 <- L341-L341
    r1 = (q / a)
    # B004 <- L342-L346
    if (q != 0.0):
        r2 = (c / q)
    else:
        r2 = F_1PE36
    return r1, r2

def tridiag(a, b, c, r, u, n):
    """L351-L398 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    gam = np.empty((n,), dtype=np.float64)
    bet = 0.0
    j = 0
    # B001 <- L387-L387
    bet = b[0]
    # B002 <- L388-L388
    u[0] = (r[0] / bet)
    # B003 <- L389-L393
    for j in range(2, n + 1):
        gam[j - 1] = (c[(j - 1) - 1] / bet)
        bet = (b[j - 1] - (a[j - 1] * gam[j - 1]))
        u[j - 1] = (((r[j - 1] - (a[j - 1] * u[(j - 1) - 1]))) / bet)
    # B004 <- L394-L396
    for j in range((n - 1), 1 - 1, (-1)):
        u[j - 1] = (u[j - 1] - (gam[(j + 1) - 1] * u[(j + 1) - 1]))
    return u

def tridiag_2eq(a1, b11, b12, c1, d1, a2, b21, b22, c2, d2, t, q, n):
    """L401-L504 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    i = 0
    ainv = 0.0
    binv = 0.0
    cinv = 0.0
    dinv = 0.0
    det = 0.0
    e11 = np.empty(((NLEVMLCAN) - (0) + 1,), dtype=np.float64)
    e12 = np.empty(((NLEVMLCAN) - (0) + 1,), dtype=np.float64)
    f1 = np.empty(((NLEVMLCAN) - (0) + 1,), dtype=np.float64)
    e21 = np.empty(((NLEVMLCAN) - (0) + 1,), dtype=np.float64)
    e22 = np.empty(((NLEVMLCAN) - (0) + 1,), dtype=np.float64)
    f2 = np.empty(((NLEVMLCAN) - (0) + 1,), dtype=np.float64)
    # B001 <- L449-L449
    e11[(0) - (0)] = 0.0
    # B002 <- L450-L450
    e12[(0) - (0)] = 0.0
    # B003 <- L451-L451
    e21[(0) - (0)] = 0.0
    # B004 <- L452-L452
    e22[(0) - (0)] = 0.0
    # B005 <- L453-L453
    f1[(0) - (0)] = 0.0
    # B006 <- L454-L454
    f2[(0) - (0)] = 0.0
    # B007 <- L456-L489
    for i in range(1, n + 1):
        ainv = (b11[i - 1] - (a1[i - 1] * e11[((i - 1)) - (0)]))
        binv = (b12[i - 1] - (a1[i - 1] * e12[((i - 1)) - (0)]))
        cinv = (b21[i - 1] - (a2[i - 1] * e21[((i - 1)) - (0)]))
        dinv = (b22[i - 1] - (a2[i - 1] * e22[((i - 1)) - (0)]))
        det = ((ainv * dinv) - (binv * cinv))
        e11[(i) - (0)] = ((dinv * c1[i - 1]) / det)
        e12[(i) - (0)] = (-((binv * c2[i - 1]) / det))
        e21[(i) - (0)] = (-((cinv * c1[i - 1]) / det))
        e22[(i) - (0)] = ((ainv * c2[i - 1]) / det)
        f1[(i) - (0)] = ((((dinv * ((d1[i - 1] - (a1[i - 1] * f1[((i - 1)) - (0)])))) - (binv * ((d2[i - 1] - (a2[i - 1] * f2[((i - 1)) - (0)])))))) / det)
        f2[(i) - (0)] = ((((-(cinv * ((d1[i - 1] - (a1[i - 1] * f1[((i - 1)) - (0)]))))) + (ainv * ((d2[i - 1] - (a2[i - 1] * f2[((i - 1)) - (0)])))))) / det)
    # B008 <- L493-L493
    i = n
    # B009 <- L494-L494
    t[i - 1] = f1[(i) - (0)]
    # B010 <- L495-L495
    q[i - 1] = f2[(i) - (0)]
    # B011 <- L499-L502
    for i in range((n - 1), 1 - 1, (-1)):
        t[i - 1] = ((f1[(i) - (0)] - (e11[(i) - (0)] * t[(i + 1) - 1])) - (e12[(i) - (0)] * q[(i + 1) - 1]))
        q[i - 1] = ((f2[(i) - (0)] - (e21[(i) - (0)] * t[(i + 1) - 1])) - (e22[(i) - (0)] * q[(i + 1) - 1]))
    return t, q

def log_gamma_function(x):
    """L507-L538 function (machine-translated)."""
    gammaln = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    coef = np.array([76.18009172947146, - 86.50532032941677, 24.01409824083091, - 1.231739572450155, 0.1208650973866179E-02, - 0.5395239384953E-05])
    stp = np.float64('2.5066282746310005')
    y = 0.0
    tmp = 0.0
    ser = 0.0
    j = 0
    # B001 <- L528-L528
    y = x
    # B002 <- L529-L529
    tmp = (x + F_5P5)
    # B003 <- L530-L530
    tmp = ((((x + 0.5)) * math.log(tmp)) - tmp)
    # B004 <- L531-L531
    ser = F_1P000000000190015
    # B005 <- L532-L535
    for j in range(1, I_6 + 1):
        y = (y + 1.0)
        ser = (ser + (coef[j - 1] / y))
    # B006 <- L536-L536
    gammaln = (tmp + math.log(((stp * ser) / x)))
    return gammaln

def beta_function(a, b):
    """L541-L559 function (machine-translated)."""
    beta = 0.0
    # B001 <- L557-L557
    beta = math.exp(((log_gamma_function(a) + log_gamma_function(b)) - log_gamma_function((a + b))))
    return beta

def beta_distribution_pdf(a, b, x):
    """L562-L581 function (machine-translated)."""
    beta_pdf = 0.0
    # B001 <- L579-L579
    beta_pdf = ((((1.0 / beta_function(a, b))) * (x ** ((a - 1.0)))) * (((1.0 - x)) ** ((b - 1.0))))
    return beta_pdf

def beta_distribution_cdf(a, b, x):
    """L584-L615 function (machine-translated)."""
    beta_cdf = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    bt = 0.0
    # B001 <- L603-L608
    if ((x == 0.0) or (x == 1.0)):
        bt = 0.0
    else:
        bt = math.exp(((((log_gamma_function((a + b)) - log_gamma_function(a)) - log_gamma_function(b)) + (a * math.log(x))) + (b * math.log((1.0 - x)))))
    # B002 <- L609-L613
    if (x < (((a + 1.0)) / (((a + b) + F_2P)))):
        beta_cdf = ((bt * beta_function_incomplete_cf(a, b, x)) / a)
    else:
        beta_cdf = (1.0 - ((bt * beta_function_incomplete_cf(b, a, (1.0 - x))) / b))
    return beta_cdf

def beta_function_incomplete_cf(a, b, x):
    """L618-L674 function (machine-translated)."""
    betacf = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    maxit = 100
    eps = np.float64('3.E-07')
    fpmin = np.float64('1.E-30')
    m = 0
    m2 = 0
    qab = 0.0
    qap = 0.0
    qam = 0.0
    c = 0.0
    d = 0.0
    h = 0.0
    aa = 0.0
    del_ = 0.0
    # B001 <- L642-L642
    qab = (a + b)
    # B002 <- L643-L643
    qap = (a + 1.0)
    # B003 <- L644-L644
    qam = (a - 1.0)
    # B004 <- L645-L645
    c = 1.0
    # B005 <- L646-L646
    d = (1.0 - ((qab * x) / qap))
    # B006 <- L647-L647
    if (abs(d) < fpmin):
        d = fpmin
    # B007 <- L648-L648
    d = (1.0 / d)
    # B008 <- L649-L649
    h = d
    # B009 <- L650-L671
    for m in range(1, maxit + 1):
        m2 = (2 * m)
        aa = (((np.float64(m) * ((b - np.float64(m)))) * x) / ((((qam + np.float64(m2))) * ((a + np.float64(m2))))))
        d = (1.0 + (aa * d))
        if (abs(d) < fpmin):
            d = fpmin
        c = (1.0 + (aa / c))
        if (abs(c) < fpmin):
            c = fpmin
        d = (1.0 / d)
        h = ((h * d) * c)
        aa = (-(((((a + np.float64(m))) * ((qab + np.float64(m)))) * x) / ((((qap + np.float64(m2))) * ((a + np.float64(m2)))))))
        d = (1.0 + (aa * d))
        if (abs(d) < fpmin):
            d = fpmin
        c = (1.0 + (aa / c))
        if (abs(c) < fpmin):
            c = fpmin
        d = (1.0 / d)
        del_ = (d * c)
        h = (h * del_)
        if (abs((del_ - 1.0)) < eps):
            betacf = h
            return betacf
    # B010 <- L672-L672
    raise RuntimeError('endrun')  # endrun (infra stub)
    return betacf
