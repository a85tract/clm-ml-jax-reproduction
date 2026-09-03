"""Machine-translated from MLCanopyTurbulenceMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call canopyturbulence before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
import re as _re
from typing import Any

import numpy as np

from mlcanopyturbulencemod_constants import *  # noqa: F401,F403
from mlcanopyturbulencemod_use_constants import *  # noqa: F401,F403
import clm_time_manager_numpy as _clm
import clm_varcon_numpy as _clm_varcon
import mlcanopyfluxestype_numpy as _mlca
import mlclm_varcon_numpy as _mlcl
import mlclm_varctl_numpy as _mlc
import mlmathtoolsmod_numpy as _mlm
import spmdmod_numpy as _spmdmod

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'canopyturbulence': {'kind': 'subroutine', 'public': True, 'args': [{'name': 'nstep_ml', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'hf2008': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'nstep_ml', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'getobu': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'obufunc': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'ic', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'il', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'obu_val', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'obu_dif', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'getbeta': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'beta_neutral', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'lcl', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'beta', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'getprsc': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'beta_neutral', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'beta_neutral_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'lcl', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'prsc', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'getpsirsl': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'za', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'hc', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'disp', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'obu', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'beta', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'prsc', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'psim', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}, {'name': 'psic', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}, {'name': 'psim2', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}, {'name': 'psim_hat2', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'phim_monin_obukhov': {'kind': 'function', 'public': False, 'args': [{'name': 'zeta', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'phi', 'result_dtype': 'float64'}, 'phic_monin_obukhov': {'kind': 'function', 'public': False, 'args': [{'name': 'zeta', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'phi', 'result_dtype': 'float64'}, 'psim_monin_obukhov': {'kind': 'function', 'public': False, 'args': [{'name': 'zeta', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'psi', 'result_dtype': 'float64'}, 'psic_monin_obukhov': {'kind': 'function', 'public': False, 'args': [{'name': 'zeta', 'dtype': 'float64', 'intent': 'IN', 'optional': False}], 'result': 'psi', 'result_dtype': 'float64'}, 'lookuppsihat': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'zdt', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'dtl', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'zdtgrid', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nZ'}, {'lb': '1', 'ub': '1'}]}, {'name': 'dtlgrid', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '1'}, {'lb': '1', 'ub': 'nL'}]}, {'name': 'psigrid', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'nZ'}, {'lb': '1', 'ub': 'nL'}]}, {'name': 'psihat', 'dtype': 'float64', 'intent': 'OUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'roughnesslength': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'windprofile': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'lm_over_beta', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'aerodynamicconductance': {'kind': 'subroutine', 'public': False, 'args': [{'name': 'p', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'lm_over_beta', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'lookuppsihatini': {'kind': 'subroutine', 'public': True, 'args': [], 'result': None, 'result_dtype': None}}

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


def canopyturbulence(nstep_ml, num_filter, filter, mlcanopy_inst):
    """L41-L73 subroutine (machine-translated)."""
    # B001 <- L60-L71
    if (_mlc.turb_type == 1):
        mlcanopy_inst = hf2008(nstep_ml, num_filter, filter, mlcanopy_inst)
    else:
        raise RuntimeError('endrun')  # endrun (infra stub)
    return mlcanopy_inst

def hf2008(nstep_ml, num_filter, filter, mlcanopy_inst):
    """L76-L210 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    ic = 0
    lm = 0.0
    lm_over_beta = 0.0
    eta = 0.0
    nstep = 0
    # B001 <- L107-L209
    pref = mlcanopy_inst.pref_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    ztop = mlcanopy_inst.ztop_canopy
    lai = mlcanopy_inst.lai_canopy
    sai = mlcanopy_inst.sai_canopy
    zw = mlcanopy_inst.zw_profile
    tair = mlcanopy_inst.tair_profile
    eair = mlcanopy_inst.eair_profile
    lc = mlcanopy_inst.lc_canopy
    taf = mlcanopy_inst.taf_canopy
    qaf = mlcanopy_inst.qaf_canopy
    mflx = mlcanopy_inst.mflx_profile
    zdisp = mlcanopy_inst.zdisp_canopy
    beta = mlcanopy_inst.beta_canopy
    prsc = mlcanopy_inst.prsc_canopy
    ustar = mlcanopy_inst.ustar_canopy
    gac_to_hc = mlcanopy_inst.gac_to_hc_canopy
    obu = mlcanopy_inst.obu_canopy
    z0m = mlcanopy_inst.z0m_canopy
    uaf = mlcanopy_inst.uaf_canopy
    wind = mlcanopy_inst.wind_profile
    gac0 = mlcanopy_inst.gac0_soil
    gac = mlcanopy_inst.gac_profile
    kc_eddy = mlcanopy_inst.kc_eddy_profile
    nstep = _clm.get_nstep()
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        lc[p - 1] = (ztop[p - 1] / ((_mlcl.cd * ((lai[p - 1] + sai[p - 1])))))
        taf[p - 1] = tair[p - 1, ntop[p - 1] - 1]
        qaf[p - 1] = (((_mlcl.mmh2o / _mlcl.mmdry) * eair[p - 1, ntop[p - 1] - 1]) / ((pref[p - 1] - (((1.0 - (_mlcl.mmh2o / _mlcl.mmdry))) * eair[p - 1, ntop[p - 1] - 1]))))
        mlcanopy_inst = getobu(p, mlcanopy_inst)
        mlcanopy_inst = roughnesslength(p, mlcanopy_inst)
        lm = ((F_2P * (beta[p - 1] * (beta[p - 1] * beta[p - 1]))) * lc[p - 1])
        eta = ((beta[p - 1] / lm) * ztop[p - 1])
        if (eta >= _mlcl.eta_max):
            pass  # write(iulog,...) log — no dataflow
            pass  # write(iulog,...) log — no dataflow
            pass  # write(iulog,...) log — no dataflow
        lm_over_beta = (ztop[p - 1] / eta)
        mlcanopy_inst = windprofile(p, lm_over_beta, mlcanopy_inst)
        for ic in range(1, ncan[p - 1] + 1):
            if (zw[p - 1, (ic) - (0)] > ztop[p - 1]):
                mflx[p - 1, ic - 1] = (-(ustar[p - 1] * ustar[p - 1]))
            else:
                mflx[p - 1, ic - 1] = (-(((ustar[p - 1] * ustar[p - 1])) * math.exp(((F_2P * ((zw[p - 1, (ic) - (0)] - ztop[p - 1]))) / lm_over_beta))))
        mlcanopy_inst = aerodynamicconductance(p, lm_over_beta, mlcanopy_inst)
    return mlcanopy_inst

def getobu(p, mlcanopy_inst):
    """L213-L262 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    ic = 0
    il = 0
    obu0 = 0.0
    obu1 = 0.0
    tol = 0.0
    dummy = 0.0
    # B001 <- L235-L261
    obu = mlcanopy_inst.obu_canopy
    ic = 0
    il = 0
    obu0 = F_100P
    obu1 = (-F_100P)
    tol = F_0P1
    dummy = _mlm.hybrid('GetObu', p, ic, il, mlcanopy_inst, obufunc, obu0, obu1, tol)
    return mlcanopy_inst

def obufunc(p, ic, il, mlcanopy_inst, obu_val):
    """L265-L424 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    obu_dif = 0.0
    obu_cur = 0.0
    obu_new = 0.0
    c1 = 0.0
    beta_neutral = 0.0
    hc_minus_d = 0.0
    psim = 0.0
    psic = 0.0
    dum1 = 0.0
    dum2 = 0.0
    zlog = 0.0
    tstar = 0.0
    qstar = 0.0
    tvstar = 0.0
    obu_min_stable = 0.0
    obu_max_unstable = 0.0
    lcl = 0.0
    beta_hf = 0.0
    beta_norsl = 0.0
    # B001 <- L307-L423
    zref = mlcanopy_inst.zref_forcing
    uref = mlcanopy_inst.uref_forcing
    thref = mlcanopy_inst.thref_forcing
    thvref = mlcanopy_inst.thvref_forcing
    qref = mlcanopy_inst.qref_forcing
    rhomol = mlcanopy_inst.rhomol_forcing
    ztop = mlcanopy_inst.ztop_canopy
    lai = mlcanopy_inst.lai_canopy
    sai = mlcanopy_inst.sai_canopy
    lc = mlcanopy_inst.lc_canopy
    taf = mlcanopy_inst.taf_canopy
    qaf = mlcanopy_inst.qaf_canopy
    zdisp = mlcanopy_inst.zdisp_canopy
    beta = mlcanopy_inst.beta_canopy
    prsc = mlcanopy_inst.prsc_canopy
    ustar = mlcanopy_inst.ustar_canopy
    gac_to_hc = mlcanopy_inst.gac_to_hc_canopy
    obu = mlcanopy_inst.obu_canopy
    obu_cur = obu_val
    obu_min_stable = (lc[p - 1] / _mlcl.lcl_max)
    obu_max_unstable = (lc[p - 1] / _mlcl.lcl_min)
    if (obu_cur >= 0.0):
        obu_cur = _f_max(obu_cur, obu_min_stable)
    else:
        obu_cur = _f_min(obu_cur, obu_max_unstable)
    lcl = (lc[p - 1] / obu_cur)
    c1 = (((_clm_varcon.vkc / math.log((((ztop[p - 1] + _mlcl.z0mg)) / _mlcl.z0mg)))) * ((_clm_varcon.vkc / math.log((((ztop[p - 1] + _mlcl.z0mg)) / _mlcl.z0mg)))))
    beta_neutral = _f_min(math.sqrt((c1 + (_mlcl.cr * ((lai[p - 1] + sai[p - 1]))))), _mlcl.beta_neutral_max)
    beta_hf = getbeta(beta_neutral, lcl)
    beta_norsl = getbeta((_clm_varcon.vkc / F_2P), lcl)
    if (lcl > _mlcl.ah12[1]):
        beta[p - 1] = beta_hf
    else:
        beta[p - 1] = (beta_norsl + (((beta_hf - beta_norsl)) / ((1 + (_mlcl.ah12[0] * (abs((lcl - _mlcl.ah12[1])) ** _mlcl.ah12[2]))))))
    hc_minus_d = ((beta[p - 1] * beta[p - 1]) * lc[p - 1])
    if (_mlc.sparse_canopy_type == 1):
        hc_minus_d = (hc_minus_d * ((1.0 - math.exp((-((F_0P25 * ((lai[p - 1] + sai[p - 1]))) / (beta[p - 1] * beta[p - 1])))))))
    hc_minus_d = _f_min(ztop[p - 1], hc_minus_d)
    zdisp[p - 1] = (ztop[p - 1] - hc_minus_d)
    if (((zref[p - 1] - zdisp[p - 1])) < 0.0):
        raise RuntimeError('endrun')  # endrun (infra stub)
    prsc[p - 1] = getprsc(beta_neutral, _mlcl.beta_neutral_max, lcl)
    psim, psic, dum1, dum2 = getpsirsl(zref[p - 1], ztop[p - 1], zdisp[p - 1], obu_cur, beta[p - 1], prsc[p - 1])
    zlog = math.log((((zref[p - 1] - zdisp[p - 1])) / ((ztop[p - 1] - zdisp[p - 1]))))
    ustar[p - 1] = ((uref[p - 1] * _clm_varcon.vkc) / ((zlog + psim)))
    tstar = ((((thref[p - 1] - taf[p - 1])) * _clm_varcon.vkc) / ((zlog + psic)))
    qstar = ((((qref[p - 1] - qaf[p - 1])) * _clm_varcon.vkc) / ((zlog + psic)))
    gac_to_hc[p - 1] = (((rhomol[p - 1] * _clm_varcon.vkc) * ustar[p - 1]) / ((zlog + psic)))
    obu[p - 1] = obu_cur
    tvstar = (tstar + ((F_0P61 * thref[p - 1]) * qstar))
    obu_new = (((ustar[p - 1] * ustar[p - 1]) * thvref[p - 1]) / (((_clm_varcon.vkc * _clm_varcon.grav) * tvstar)))
    obu_dif = (obu_new - obu_val)
    return mlcanopy_inst, obu_dif

def getbeta(beta_neutral, lcl):
    """L427-L480 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    beta = 0.0
    aa = 0.0
    bb = 0.0
    cc = 0.0
    dd = 0.0
    qq = 0.0
    rr = 0.0
    y = 0.0
    fy = 0.0
    err = 0.0
    # B001 <- L446-L469
    if (lcl <= 0.0):
        aa = 1.0
        bb = ((F_16P * lcl) * ((beta_neutral * beta_neutral) * (beta_neutral * beta_neutral)))
        cc = (-((beta_neutral * beta_neutral) * (beta_neutral * beta_neutral)))
        beta = math.sqrt(((((-bb) + math.sqrt(((bb * bb) - ((F_4P * aa) * cc))))) / ((F_2P * aa))))
    else:
        aa = (F_5P * lcl)
        bb = 0.0
        cc = 1.0
        dd = (-beta_neutral)
        qq = ((((((F_2P * (bb * (bb * bb))) - (((F_9P * aa) * bb) * cc)) + ((F_27P * ((aa * aa))) * dd))) * ((((F_2P * (bb * (bb * bb))) - (((F_9P * aa) * bb) * cc)) + ((F_27P * ((aa * aa))) * dd)))) - (F_4P * ((((bb * bb) - ((F_3P * aa) * cc))) * ((((bb * bb) - ((F_3P * aa) * cc))) * (((bb * bb) - ((F_3P * aa) * cc)))))))
        qq = math.sqrt(qq)
        rr = (0.5 * ((((qq + (F_2P * (bb * (bb * bb)))) - (((F_9P * aa) * bb) * cc)) + ((F_27P * ((aa * aa))) * dd))))
        rr = (rr ** ((1.0 / F_3P)))
        beta = ((-(((bb + rr)) / ((F_3P * aa)))) - ((((bb * bb) - ((F_3P * aa) * cc))) / (((F_3P * aa) * rr))))
    # B002 <- L473-L473
    y = (lcl * (beta * beta))
    # B003 <- L474-L474
    fy = phim_monin_obukhov(y)
    # B004 <- L475-L475
    err = ((beta * fy) - beta_neutral)
    # B005 <- L476-L478
    if (abs(err) > F_1PEM06):
        raise RuntimeError('endrun')  # endrun (infra stub)
    return beta

def getprsc(beta_neutral, beta_neutral_max, lcl):
    """L483-L511 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    prsc = 0.0
    # B001 <- L502-L502
    prsc = (_mlcl.pr0 + (_mlcl.pr1 * math.tanh((_mlcl.pr2 * lcl))))
    # B002 <- L506-L509
    if (_mlc.sparse_canopy_type == 1):
        prsc = ((((1.0 - (beta_neutral / beta_neutral_max))) * 1.0) + (((beta_neutral / beta_neutral_max)) * prsc))
    return prsc

def getpsirsl(za, hc, disp, obu, beta, prsc):
    """L514-L620 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    psim = 0.0
    psic = 0.0
    psim2 = 0.0
    psim_hat2 = 0.0
    dt = 0.0
    phim = 0.0
    phic = 0.0
    c1 = 0.0
    psim1 = 0.0
    psic1 = 0.0
    psic2 = 0.0
    psim_hat1 = 0.0
    psic_hat1 = 0.0
    psic_hat2 = 0.0
    # B001 <- L574-L574
    phim = phim_monin_obukhov((((hc - disp)) / obu))
    # B002 <- L575-L575
    c1 = (((1.0 - (_clm_varcon.vkc / (((F_2P * beta) * phim))))) * math.exp((0.5 * _mlcl.c2)))
    # B003 <- L587-L587
    dt = (hc - disp)
    # B004 <- L588-L588
    psim_hat1 = lookuppsihat((((za - hc)) / dt), (dt / obu), _mlcl.zdtgridm, _mlcl.dtlgridm, _mlcl.psigridm)
    # B005 <- L589-L589
    psim_hat2 = lookuppsihat((((hc - hc)) / dt), (dt / obu), _mlcl.zdtgridm, _mlcl.dtlgridm, _mlcl.psigridm)
    # B006 <- L590-L590
    psim_hat1 = (psim_hat1 * c1)
    # B007 <- L591-L591
    psim_hat2 = (psim_hat2 * c1)
    # B008 <- L596-L596
    psim1 = psim_monin_obukhov((((za - disp)) / obu))
    # B009 <- L597-L597
    psim2 = psim_monin_obukhov((((hc - disp)) / obu))
    # B010 <- L602-L602
    psim = (((((-psim1) + psim2) + psim_hat1) - psim_hat2) + (_clm_varcon.vkc / beta))
    # B011 <- L607-L607
    phic = phic_monin_obukhov((((hc - disp)) / obu))
    # B012 <- L608-L608
    c1 = (((1.0 - ((prsc * _clm_varcon.vkc) / (((F_2P * beta) * phic))))) * math.exp((0.5 * _mlcl.c2)))
    # B013 <- L610-L610
    psic_hat1 = lookuppsihat((((za - hc)) / dt), (dt / obu), _mlcl.zdtgridh, _mlcl.dtlgridh, _mlcl.psigridh)
    # B014 <- L611-L611
    psic_hat2 = lookuppsihat((((hc - hc)) / dt), (dt / obu), _mlcl.zdtgridh, _mlcl.dtlgridh, _mlcl.psigridh)
    # B015 <- L612-L612
    psic_hat1 = (psic_hat1 * c1)
    # B016 <- L613-L613
    psic_hat2 = (psic_hat2 * c1)
    # B017 <- L615-L615
    psic1 = psic_monin_obukhov((((za - disp)) / obu))
    # B018 <- L616-L616
    psic2 = psic_monin_obukhov((((hc - disp)) / obu))
    # B019 <- L618-L618
    psic = ((((-psic1) + psic2) + psic_hat1) - psic_hat2)
    return psim, psic, psim2, psim_hat2

def phim_monin_obukhov(zeta):
    """L623-L645 function (machine-translated)."""
    phi = 0.0
    # B001 <- L639-L643
    if (zeta < 0.0):
        phi = (1.0 / math.sqrt(math.sqrt((1.0 - (F_16P * zeta)))))
    else:
        phi = (1.0 + (F_5P * zeta))
    return phi

def phic_monin_obukhov(zeta):
    """L648-L670 function (machine-translated)."""
    phi = 0.0
    # B001 <- L664-L668
    if (zeta < 0.0):
        phi = (1.0 / math.sqrt((1.0 - (F_16P * zeta))))
    else:
        phi = (1.0 + (F_5P * zeta))
    return phi

def psim_monin_obukhov(zeta):
    """L673-L698 function (machine-translated)."""
    psi = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    x = 0.0
    # B001 <- L691-L696
    if (zeta < 0.0):
        x = math.sqrt(math.sqrt((1.0 - (F_16P * zeta))))
        psi = ((((F_2P * math.log((((1.0 + x)) / F_2P))) + math.log((((1.0 + (x * x))) / F_2P))) - (F_2P * math.atan(x))) + (_clm_varcon.rpi * 0.5))
    else:
        psi = (-(F_5P * zeta))
    return psi

def psic_monin_obukhov(zeta):
    """L701-L725 function (machine-translated)."""
    psi = 0.0
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    x = 0.0
    # B001 <- L718-L723
    if (zeta < 0.0):
        x = math.sqrt(math.sqrt((1.0 - (F_16P * zeta))))
        psi = (F_2P * math.log((((1.0 + (x * x))) / F_2P)))
    else:
        psi = (-(F_5P * zeta))
    return psi

def lookuppsihat(zdt, dtl, zdtgrid, dtlgrid, psigrid):
    """L728-L828 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    psihat = 0.0
    ii = 0
    jj = 0
    l1 = 0
    l2 = 0
    z1 = 0
    z2 = 0
    wl1 = 0.0
    wl2 = 0.0
    wz1 = 0.0
    wz2 = 0.0
    # B001 <- L769-L769
    l1 = 0
    # B002 <- L769-L769
    l2 = 0
    # B003 <- L770-L789
    if (dtl <= dtlgrid[0, 0]):
        l1 = 1
        l2 = 1
        wl1 = 0.5
        wl2 = 0.5
    elif (dtl > dtlgrid[0, NL - 1]):
        l1 = NL
        l2 = NL
        wl1 = 0.5
        wl2 = 0.5
    else:
        for jj in range(1, (NL - 1) + 1):
            if (((dtl <= dtlgrid[0, (jj + 1) - 1])) and ((dtl > dtlgrid[0, jj - 1]))):
                l1 = jj
                l2 = (jj + 1)
                wl1 = (((dtlgrid[0, l2 - 1] - dtl)) / ((dtlgrid[0, l2 - 1] - dtlgrid[0, l1 - 1])))
                wl2 = (1.0 - wl1)
    # B004 <- L791-L793
    if ((l1 == 0) or (l2 == 0)):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B005 <- L797-L797
    z1 = 0
    # B006 <- L797-L797
    z2 = 0
    # B007 <- L798-L817
    if (zdt > zdtgrid[0, 0]):
        z1 = 1
        z2 = 1
        wz1 = 0.5
        wz2 = 0.5
    elif (zdt < zdtgrid[NZ - 1, 0]):
        z1 = NZ
        z2 = NZ
        wz1 = 0.5
        wz2 = 0.5
    else:
        for ii in range(1, (NZ - 1) + 1):
            if (((zdt >= zdtgrid[(ii + 1) - 1, 0])) and ((zdt < zdtgrid[ii - 1, 0]))):
                z1 = ii
                z2 = (ii + 1)
                wz1 = (((zdt - zdtgrid[(ii + 1) - 1, 0])) / ((zdtgrid[ii - 1, 0] - zdtgrid[(ii + 1) - 1, 0])))
                wz2 = (1.0 - wz1)
    # B008 <- L819-L821
    if ((z1 == 0) or (z2 == 0)):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B009 <- L825-L826
    psihat = (((((wz1 * wl1) * psigrid[z1 - 1, l1 - 1]) + ((wz2 * wl1) * psigrid[z2 - 1, l1 - 1])) + ((wz1 * wl2) * psigrid[z1 - 1, l2 - 1])) + ((wz2 * wl2) * psigrid[z2 - 1, l2 - 1]))
    return psihat

def roughnesslength(p, mlcanopy_inst):
    """L831-L928 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    hc_minus_d = 0.0
    psim = 0.0
    psic = 0.0
    psim_hc = 0.0
    psim_hat_hc = 0.0
    exp1 = 0.0
    exp2 = 0.0
    aval = 0.0
    bval = 0.0
    cval = 0.0
    z0m_aval = 0.0
    z0m_bval = 0.0
    z0m_cval = 0.0
    psim_z0m_aval = 0.0
    psim_z0m_bval = 0.0
    psim_z0m_cval = 0.0
    fa = 0.0
    fb = 0.0
    fc = 0.0
    err = 0.0
    n = 0
    nmax = 0
    # B001 <- L865-L927
    zref = mlcanopy_inst.zref_forcing
    ztop = mlcanopy_inst.ztop_canopy
    zdisp = mlcanopy_inst.zdisp_canopy
    obu = mlcanopy_inst.obu_canopy
    beta = mlcanopy_inst.beta_canopy
    prsc = mlcanopy_inst.prsc_canopy
    z0m = mlcanopy_inst.z0m_canopy
    psim, psic, psim_hc, psim_hat_hc = getpsirsl(zref[p - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
    hc_minus_d = (ztop[p - 1] - zdisp[p - 1])
    exp1 = math.exp((-(_clm_varcon.vkc / beta[p - 1])))
    exp2 = math.exp(psim_hat_hc)
    aval = ztop[p - 1]
    bval = 0.0
    err = F_0P001
    nmax = I_20
    psim_z0m_aval = psim_monin_obukhov((aval / obu[p - 1]))
    z0m_aval = (((hc_minus_d * exp1) * math.exp(((-psim_hc) + psim_z0m_aval))) * exp2)
    fa = (z0m_aval - aval)
    psim_z0m_bval = psim_monin_obukhov((bval / obu[p - 1]))
    z0m_bval = (((hc_minus_d * exp1) * math.exp(((-psim_hc) + psim_z0m_bval))) * exp2)
    fb = (z0m_bval - bval)
    if ((fa * fb) > 0.0):
        raise RuntimeError('endrun')  # endrun (infra stub)
    n = 1
    while ((abs((bval - aval)) > err) and (n <= nmax)):
        cval = (((aval + bval)) / F_2P)
        psim_z0m_cval = psim_monin_obukhov((cval / obu[p - 1]))
        z0m_cval = (((hc_minus_d * exp1) * math.exp(((-psim_hc) + psim_z0m_cval))) * exp2)
        fc = (z0m_cval - cval)
        if ((fa * fc) < 0.0):
            bval = cval
            fb = fc
        else:
            aval = cval
            fa = fc
        n = (n + 1)
    if (n > nmax):
        raise RuntimeError('endrun')  # endrun (infra stub)
    z0m[p - 1] = cval
    return mlcanopy_inst

def windprofile(p, lm_over_beta, mlcanopy_inst):
    """L931-L991 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    ic = 0
    psim = 0.0
    psic = 0.0
    dum1 = 0.0
    dum2 = 0.0
    zlog_m = 0.0
    # B001 <- L954-L990
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    zs = mlcanopy_inst.zs_profile
    ztop = mlcanopy_inst.ztop_canopy
    zdisp = mlcanopy_inst.zdisp_canopy
    obu = mlcanopy_inst.obu_canopy
    beta = mlcanopy_inst.beta_canopy
    prsc = mlcanopy_inst.prsc_canopy
    ustar = mlcanopy_inst.ustar_canopy
    uaf = mlcanopy_inst.uaf_canopy
    wind = mlcanopy_inst.wind_profile
    for ic in range((ntop[p - 1] + 1), ncan[p - 1] + 1):
        psim, psic, dum1, dum2 = getpsirsl(zs[p - 1, ic - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
        zlog_m = math.log((((zs[p - 1, ic - 1] - zdisp[p - 1])) / ((ztop[p - 1] - zdisp[p - 1]))))
        wind[p - 1, ic - 1] = ((ustar[p - 1] / _clm_varcon.vkc) * ((zlog_m + psim)))
    uaf[p - 1] = (ustar[p - 1] / beta[p - 1])
    for ic in range(1, ntop[p - 1] + 1):
        wind[p - 1, ic - 1] = (uaf[p - 1] * math.exp((((zs[p - 1, ic - 1] - ztop[p - 1])) / lm_over_beta)))
    return mlcanopy_inst

def aerodynamicconductance(p, lm_over_beta, mlcanopy_inst):
    """L994-L1180 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    ic = 0
    psim1 = 0.0
    psim2 = 0.0
    psic = 0.0
    psic1 = 0.0
    psic2 = 0.0
    dum1 = 0.0
    dum2 = 0.0
    zlog_m = 0.0
    zlog_c = 0.0
    zu = 0.0
    zl = 0.0
    res = 0.0
    ustar_g = 0.0
    z0cg = 0.0
    sumres = 0.0
    gac_above_foliage = 0.0
    gac_below_foliage = 0.0
    # B001 <- L1027-L1179
    zref = mlcanopy_inst.zref_forcing
    rhomol = mlcanopy_inst.rhomol_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    ztop = mlcanopy_inst.ztop_canopy
    zdisp = mlcanopy_inst.zdisp_canopy
    obu = mlcanopy_inst.obu_canopy
    beta = mlcanopy_inst.beta_canopy
    prsc = mlcanopy_inst.prsc_canopy
    ustar = mlcanopy_inst.ustar_canopy
    gac_to_hc = mlcanopy_inst.gac_to_hc_canopy
    zs = mlcanopy_inst.zs_profile
    wind = mlcanopy_inst.wind_profile
    gac0 = mlcanopy_inst.gac0_soil
    gac = mlcanopy_inst.gac_profile
    kc_eddy = mlcanopy_inst.kc_eddy_profile
    for ic in range((ntop[p - 1] + 1), (ncan[p - 1] - 1) + 1):
        psim1, psic1, dum1, dum2 = getpsirsl(zs[p - 1, ic - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
        psim2, psic2, dum1, dum2 = getpsirsl(zs[p - 1, (ic + 1) - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
        psic = (psic2 - psic1)
        zlog_c = math.log((((zs[p - 1, (ic + 1) - 1] - zdisp[p - 1])) / ((zs[p - 1, ic - 1] - zdisp[p - 1]))))
        gac[p - 1, ic - 1] = (((rhomol[p - 1] * _clm_varcon.vkc) * ustar[p - 1]) / ((zlog_c + psic)))
    ic = int(ncan[p - 1])
    psim1, psic1, dum1, dum2 = getpsirsl(zs[p - 1, ic - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
    psim2, psic2, dum1, dum2 = getpsirsl(zref[p - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
    psic = (psic2 - psic1)
    zlog_c = math.log((((zref[p - 1] - zdisp[p - 1])) / ((zs[p - 1, ic - 1] - zdisp[p - 1]))))
    gac[p - 1, ic - 1] = (((rhomol[p - 1] * _clm_varcon.vkc) * ustar[p - 1]) / ((zlog_c + psic)))
    ic = int(ntop[p - 1])
    psim1, psic1, dum1, dum2 = getpsirsl(ztop[p - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
    psim2, psic2, dum1, dum2 = getpsirsl(zs[p - 1, (ic + 1) - 1], ztop[p - 1], zdisp[p - 1], obu[p - 1], beta[p - 1], prsc[p - 1])
    psic = (psic2 - psic1)
    zlog_c = math.log((((zs[p - 1, (ic + 1) - 1] - zdisp[p - 1])) / ((ztop[p - 1] - zdisp[p - 1]))))
    gac_above_foliage = (((rhomol[p - 1] * _clm_varcon.vkc) * ustar[p - 1]) / ((zlog_c + psic)))
    sumres = (1.0 / gac_above_foliage)
    for ic in range((ntop[p - 1] + 1), ncan[p - 1] + 1):
        sumres = (sumres + (1.0 / gac[p - 1, ic - 1]))
    if (abs(((1.0 / sumres) - gac_to_hc[p - 1])) > F_1PEM06):
        raise RuntimeError('endrun')  # endrun (infra stub)
    for ic in range(1, (ntop[p - 1] - 1) + 1):
        zl = (zs[p - 1, ic - 1] - ztop[p - 1])
        zu = (zs[p - 1, (ic + 1) - 1] - ztop[p - 1])
        res = ((prsc[p - 1] / ((beta[p - 1] * ustar[p - 1]))) * ((math.exp((-(zl / lm_over_beta))) - math.exp((-(zu / lm_over_beta))))))
        gac[p - 1, ic - 1] = (rhomol[p - 1] / res)
    ic = int(ntop[p - 1])
    zl = (zs[p - 1, ic - 1] - ztop[p - 1])
    zu = (ztop[p - 1] - ztop[p - 1])
    res = ((prsc[p - 1] / ((beta[p - 1] * ustar[p - 1]))) * ((math.exp((-(zl / lm_over_beta))) - math.exp((-(zu / lm_over_beta))))))
    gac_below_foliage = (rhomol[p - 1] / res)
    gac[p - 1, ic - 1] = (1.0 / (((1.0 / gac_below_foliage) + (1.0 / gac_above_foliage))))
    z0cg = (F_0P1 * _mlcl.z0mg)
    if ((_mlcl.z0mg > zs[p - 1, 0]) or (z0cg > zs[p - 1, 0])):
        raise RuntimeError('endrun')  # endrun (infra stub)
    if (_mlc.hf_extension_type == 1):
        zl = (z0cg - ztop[p - 1])
        zu = (zs[p - 1, 0] - ztop[p - 1])
        res = ((prsc[p - 1] / ((beta[p - 1] * ustar[p - 1]))) * ((math.exp((-(zl / lm_over_beta))) - math.exp((-(zu / lm_over_beta))))))
        gac0[p - 1] = (rhomol[p - 1] / res)
    elif (_mlc.hf_extension_type == 2):
        zlog_m = math.log((zs[p - 1, 0] / _mlcl.z0mg))
        ustar_g = ((_f_max(wind[p - 1, 0], F_0P1) * _clm_varcon.vkc) / zlog_m)
        gac0[p - 1] = (((rhomol[p - 1] * _clm_varcon.vkc) * ustar_g) / zlog_m)
    res = _f_min((rhomol[p - 1] / gac0[p - 1]), _mlcl.ra_max)
    gac0[p - 1] = (rhomol[p - 1] / res)
    for ic in range(1, ncan[p - 1] + 1):
        res = _f_min((rhomol[p - 1] / gac[p - 1, ic - 1]), _mlcl.ra_max)
        gac[p - 1, ic - 1] = (rhomol[p - 1] / res)
    for ic in range(1, ncan[p - 1] + 1):
        if (ic == ncan[p - 1]):
            kc_eddy[p - 1, ic - 1] = ((gac[p - 1, ic - 1] / rhomol[p - 1]) * ((zref[p - 1] - zs[p - 1, ic - 1])))
        else:
            kc_eddy[p - 1, ic - 1] = ((gac[p - 1, ic - 1] / rhomol[p - 1]) * ((zs[p - 1, (ic + 1) - 1] - zs[p - 1, ic - 1])))
    return mlcanopy_inst

def lookuppsihatini():
    """L1183-L1296 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    locfn = ''
    ncid = _new_derived()
    dimid = 0
    readv = False
    zdtgridm_nc = np.empty((NZ,), dtype=np.float64)
    dtlgridm_nc = np.empty((NL,), dtype=np.float64)
    psigridm_nc = np.empty((NL, NZ,), dtype=np.float64)
    zdtgridh_nc = np.empty((NZ,), dtype=np.float64)
    dtlgridh_nc = np.empty((NL,), dtype=np.float64)
    psigridh_nc = np.empty((NL, NZ,), dtype=np.float64)
    nz_nc = 0
    nl_nc = 0
    ii = 0
    jj = 0
    # B001 <- L1219-L1221
    if _spmdmod.masterproc:
        pass  # write(iulog,...) log — no dataflow
    # B002 <- L1225-L1225 AGENT_QUEUE: call to external subroutine 'getfil'
    raise NotImplementedError("call to external subroutine 'getfil'")  # B002
    # B003 <- L1229-L1229
    pass  # ncd_pio_openfile (infra stub)
    # B004 <- L1233-L1233
    pass  # ncd_inqdid (infra stub)
    # B005 <- L1234-L1234
    pass  # ncd_inqdlen (infra stub)
    # B006 <- L1236-L1238
    if (nz_nc != NZ):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B007 <- L1240-L1240
    pass  # ncd_inqdid (infra stub)
    # B008 <- L1241-L1241
    pass  # ncd_inqdlen (infra stub)
    # B009 <- L1243-L1245
    if (nl_nc != NL):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B010 <- L1249-L1249
    pass  # ncd_io (infra stub)
    # B011 <- L1250-L1250
    if (not readv):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B012 <- L1252-L1252
    pass  # ncd_io (infra stub)
    # B013 <- L1253-L1253
    if (not readv):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B014 <- L1255-L1255
    pass  # ncd_io (infra stub)
    # B015 <- L1256-L1256
    if (not readv):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B016 <- L1258-L1258
    pass  # ncd_io (infra stub)
    # B017 <- L1259-L1259
    if (not readv):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B018 <- L1261-L1261
    pass  # ncd_io (infra stub)
    # B019 <- L1262-L1262
    if (not readv):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B020 <- L1264-L1264
    pass  # ncd_io (infra stub)
    # B021 <- L1265-L1265
    if (not readv):
        raise RuntimeError('endrun')  # endrun (infra stub)
    # B022 <- L1269-L1269
    pass  # ncd_pio_closefile (infra stub)
    # B023 <- L1271-L1273
    if _spmdmod.masterproc:
        pass  # write(iulog,...) log — no dataflow
    # B024 <- L1277-L1280
    for jj in range(1, NL + 1):
        _mlcl.dtlgridm[0, jj - 1] = dtlgridm_nc[jj - 1]
        _mlcl.dtlgridh[0, jj - 1] = dtlgridh_nc[jj - 1]
    # B025 <- L1282-L1285
    for ii in range(1, NZ + 1):
        _mlcl.zdtgridm[ii - 1, 0] = zdtgridm_nc[ii - 1]
        _mlcl.zdtgridh[ii - 1, 0] = zdtgridh_nc[ii - 1]
    # B026 <- L1287-L1292
    for ii in range(1, NZ + 1):
        for jj in range(1, NL + 1):
            _mlcl.psigridm[ii - 1, jj - 1] = psigridm_nc[jj - 1, ii - 1]
            _mlcl.psigridh[ii - 1, jj - 1] = psigridh_nc[jj - 1, ii - 1]
    # B027 <- L1294-L1294
    return 


# Flattened adapters for the differential gate (recast.transform.numpy.flat).
class _Record:
    def __init__(self, **fields):
        self.__dict__.update(fields)

def canopyturbulence_flat(nstep_ml, num_filter, filter, np_, mlcanopy_inst__beta_canopy, mlcanopy_inst__eair_profile, mlcanopy_inst__gac0_soil, mlcanopy_inst__gac_profile, mlcanopy_inst__gac_to_hc_canopy, mlcanopy_inst__kc_eddy_profile, mlcanopy_inst__lai_canopy, mlcanopy_inst__lc_canopy, mlcanopy_inst__mflx_profile, mlcanopy_inst__ncan_canopy, mlcanopy_inst__ntop_canopy, mlcanopy_inst__obu_canopy, mlcanopy_inst__pref_forcing, mlcanopy_inst__prsc_canopy, mlcanopy_inst__qaf_canopy, mlcanopy_inst__qref_forcing, mlcanopy_inst__rhomol_forcing, mlcanopy_inst__sai_canopy, mlcanopy_inst__taf_canopy, mlcanopy_inst__tair_profile, mlcanopy_inst__thref_forcing, mlcanopy_inst__thvref_forcing, mlcanopy_inst__uaf_canopy, mlcanopy_inst__uref_forcing, mlcanopy_inst__ustar_canopy, mlcanopy_inst__wind_profile, mlcanopy_inst__z0m_canopy, mlcanopy_inst__zdisp_canopy, mlcanopy_inst__zref_forcing, mlcanopy_inst__zs_profile, mlcanopy_inst__ztop_canopy, mlcanopy_inst__zw_profile, clm_time_manager__itim, clm_varcon__grav, clm_varcon__vkc, mlclm_varcon__ah12, mlclm_varcon__beta_neutral_max, mlclm_varcon__c2, mlclm_varcon__cd, mlclm_varcon__cr, mlclm_varcon__dtlgridh, mlclm_varcon__dtlgridm, mlclm_varcon__eta_max, mlclm_varcon__lcl_max, mlclm_varcon__lcl_min, mlclm_varcon__mmdry, mlclm_varcon__mmh2o, mlclm_varcon__pr0, mlclm_varcon__pr1, mlclm_varcon__pr2, mlclm_varcon__psigridh, mlclm_varcon__psigridm, mlclm_varcon__ra_max, mlclm_varcon__z0mg, mlclm_varcon__zdtgridh, mlclm_varcon__zdtgridm, mlclm_varctl__hf_extension_type, mlclm_varctl__sparse_canopy_type, mlclm_varctl__turb_type):
    mlcanopy_inst = _Record(beta_canopy=mlcanopy_inst__beta_canopy, eair_profile=mlcanopy_inst__eair_profile, gac0_soil=mlcanopy_inst__gac0_soil, gac_profile=mlcanopy_inst__gac_profile, gac_to_hc_canopy=mlcanopy_inst__gac_to_hc_canopy, kc_eddy_profile=mlcanopy_inst__kc_eddy_profile, lai_canopy=mlcanopy_inst__lai_canopy, lc_canopy=mlcanopy_inst__lc_canopy, mflx_profile=mlcanopy_inst__mflx_profile, ncan_canopy=mlcanopy_inst__ncan_canopy, ntop_canopy=mlcanopy_inst__ntop_canopy, obu_canopy=mlcanopy_inst__obu_canopy, pref_forcing=mlcanopy_inst__pref_forcing, prsc_canopy=mlcanopy_inst__prsc_canopy, qaf_canopy=mlcanopy_inst__qaf_canopy, qref_forcing=mlcanopy_inst__qref_forcing, rhomol_forcing=mlcanopy_inst__rhomol_forcing, sai_canopy=mlcanopy_inst__sai_canopy, taf_canopy=mlcanopy_inst__taf_canopy, tair_profile=mlcanopy_inst__tair_profile, thref_forcing=mlcanopy_inst__thref_forcing, thvref_forcing=mlcanopy_inst__thvref_forcing, uaf_canopy=mlcanopy_inst__uaf_canopy, uref_forcing=mlcanopy_inst__uref_forcing, ustar_canopy=mlcanopy_inst__ustar_canopy, wind_profile=mlcanopy_inst__wind_profile, z0m_canopy=mlcanopy_inst__z0m_canopy, zdisp_canopy=mlcanopy_inst__zdisp_canopy, zref_forcing=mlcanopy_inst__zref_forcing, zs_profile=mlcanopy_inst__zs_profile, ztop_canopy=mlcanopy_inst__ztop_canopy, zw_profile=mlcanopy_inst__zw_profile)
    import clm_time_manager_numpy as _clm_time_manager
    _clm_time_manager.itim = clm_time_manager__itim
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.grav = clm_varcon__grav
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.vkc = clm_varcon__vkc
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.ah12 = mlclm_varcon__ah12
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.beta_neutral_max = mlclm_varcon__beta_neutral_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.c2 = mlclm_varcon__c2
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cd = mlclm_varcon__cd
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cr = mlclm_varcon__cr
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dtlgridh = mlclm_varcon__dtlgridh
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dtlgridm = mlclm_varcon__dtlgridm
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.eta_max = mlclm_varcon__eta_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.lcl_max = mlclm_varcon__lcl_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.lcl_min = mlclm_varcon__lcl_min
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.mmdry = mlclm_varcon__mmdry
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.mmh2o = mlclm_varcon__mmh2o
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.pr0 = mlclm_varcon__pr0
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.pr1 = mlclm_varcon__pr1
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.pr2 = mlclm_varcon__pr2
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.psigridh = mlclm_varcon__psigridh
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.psigridm = mlclm_varcon__psigridm
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.ra_max = mlclm_varcon__ra_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.z0mg = mlclm_varcon__z0mg
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.zdtgridh = mlclm_varcon__zdtgridh
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.zdtgridm = mlclm_varcon__zdtgridm
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.hf_extension_type = mlclm_varctl__hf_extension_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.sparse_canopy_type = mlclm_varctl__sparse_canopy_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.turb_type = mlclm_varctl__turb_type
    _out = canopyturbulence(nstep_ml=nstep_ml, num_filter=num_filter, filter=filter, mlcanopy_inst=mlcanopy_inst)
    _out = (_out,)
    mlcanopy_inst_, = _out
    mlcanopy_inst__beta_canopy = mlcanopy_inst.beta_canopy
    mlcanopy_inst__gac0_soil = mlcanopy_inst.gac0_soil
    mlcanopy_inst__gac_profile = mlcanopy_inst.gac_profile
    mlcanopy_inst__gac_to_hc_canopy = mlcanopy_inst.gac_to_hc_canopy
    mlcanopy_inst__kc_eddy_profile = mlcanopy_inst.kc_eddy_profile
    mlcanopy_inst__lc_canopy = mlcanopy_inst.lc_canopy
    mlcanopy_inst__mflx_profile = mlcanopy_inst.mflx_profile
    mlcanopy_inst__obu_canopy = mlcanopy_inst.obu_canopy
    mlcanopy_inst__prsc_canopy = mlcanopy_inst.prsc_canopy
    mlcanopy_inst__qaf_canopy = mlcanopy_inst.qaf_canopy
    mlcanopy_inst__taf_canopy = mlcanopy_inst.taf_canopy
    mlcanopy_inst__uaf_canopy = mlcanopy_inst.uaf_canopy
    mlcanopy_inst__ustar_canopy = mlcanopy_inst.ustar_canopy
    mlcanopy_inst__wind_profile = mlcanopy_inst.wind_profile
    mlcanopy_inst__z0m_canopy = mlcanopy_inst.z0m_canopy
    mlcanopy_inst__zdisp_canopy = mlcanopy_inst.zdisp_canopy
    return mlcanopy_inst__beta_canopy, mlcanopy_inst__gac0_soil, mlcanopy_inst__gac_profile, mlcanopy_inst__gac_to_hc_canopy, mlcanopy_inst__kc_eddy_profile, mlcanopy_inst__lc_canopy, mlcanopy_inst__mflx_profile, mlcanopy_inst__obu_canopy, mlcanopy_inst__prsc_canopy, mlcanopy_inst__qaf_canopy, mlcanopy_inst__taf_canopy, mlcanopy_inst__uaf_canopy, mlcanopy_inst__ustar_canopy, mlcanopy_inst__wind_profile, mlcanopy_inst__z0m_canopy, mlcanopy_inst__zdisp_canopy

_SIGNATURES.update({
    'canopyturbulence_flat': {'kind': 'subroutine', 'args': [{'name': 'nstep_ml', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'num_filter'}]}, {'name': 'np_', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlcanopy_inst__beta_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__eair_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__gac0_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gac_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__gac_to_hc_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__kc_eddy_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lai_canopy', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lc_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__mflx_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__ncan_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ntop_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__obu_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__pref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__prsc_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qaf_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rhomol_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__sai_canopy', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__taf_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tair_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__thref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__thvref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__uaf_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__uref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ustar_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__wind_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__z0m_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zdisp_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zref_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zs_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__ztop_canopy', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zw_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}]}, {'name': 'clm_time_manager__itim', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__grav', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__vkc', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__ah12', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '3'}]}, {'name': 'mlclm_varcon__beta_neutral_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__c2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cd', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cr', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__dtlgridh', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '1'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__dtlgridm', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '1'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__eta_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__lcl_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__lcl_min', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__mmdry', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__mmh2o', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__pr0', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__pr1', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__pr2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__psigridh', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__psigridm', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__ra_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__z0mg', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__zdtgridh', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '1'}]}, {'name': 'mlclm_varcon__zdtgridm', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '1'}]}, {'name': 'mlclm_varctl__hf_extension_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__sparse_canopy_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__turb_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}], 'result': None, 'result_dtype': None},
})
