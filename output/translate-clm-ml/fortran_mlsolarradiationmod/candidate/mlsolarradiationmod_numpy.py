"""Machine-translated from MLSolarRadiationMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call solarradiation before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
import re as _re
from typing import Any

import numpy as np

from mlsolarradiationmod_constants import *  # noqa: F401,F403
from mlsolarradiationmod_use_constants import *  # noqa: F401,F403
import clm_varcon_numpy as _clm_varcon
import clm_varpar_numpy as _clm_varpar
import mlcanopyfluxestype_numpy as _mlc
import mlclm_varcon_numpy as _mlcl
import mlclm_varctl_numpy as _mlclm
import mlmathtoolsmod_numpy as _mlm
import mlpftconmod_numpy as _mlp
import patchtype_numpy as _patchtype
import pftconmod_numpy as _pftconmod

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'solarradiation': {'kind': 'subroutine', 'args': [{'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'norman': {'kind': 'subroutine', 'args': [{'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'rho', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}, {'lb': '1', 'ub': 'numrad'}]}, {'name': 'tau', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}, {'lb': '1', 'ub': 'numrad'}]}, {'name': 'omega', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}, {'lb': '1', 'ub': 'numrad'}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'twostream': {'kind': 'subroutine', 'args': [{'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'omega', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}, {'lb': '1', 'ub': 'numrad'}]}, {'name': 'avmu', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'betad', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}, {'lb': '1', 'ub': 'numrad'}]}, {'name': 'betab', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}, {'lb': '1', 'ub': 'numrad'}]}, {'name': 'clump_fac_ic', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': 'bounds % begp', 'ub': 'bounds % endp'}, {'lb': '1', 'ub': 'nlevmlcan'}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}}

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


def solarradiation(bounds, num_filter, filter, mlcanopy_inst):
    """L33-L289 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    c = 0
    ic = 0
    ib = 0
    j = 0
    angle = 0.0
    gdirj = 0.0
    wl = 0.0
    ws = 0.0
    chil = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN,), dtype=np.float64)
    phi1 = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN,), dtype=np.float64)
    phi2 = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN,), dtype=np.float64)
    gdir = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN,), dtype=np.float64)
    clump_fac_ic = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN,), dtype=np.float64)
    rho = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    tau = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    omega = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    asu = 0.0
    tmp0 = 0.0
    tmp1 = 0.0
    tmp2 = 0.0
    avmu = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN,), dtype=np.float64)
    betad = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    betab = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    # B001 <- L85-L288
    xl = _pftconmod.pftcon.xl
    rhol = _pftconmod.pftcon.rhol
    taul = _pftconmod.pftcon.taul
    rhos = _pftconmod.pftcon.rhos
    taus = _pftconmod.pftcon.taus
    clump_fac = _mlp.mlpftcon.clump_fac
    solar_zen = mlcanopy_inst.solar_zen_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    nbot = mlcanopy_inst.nbot_canopy
    dlai = mlcanopy_inst.dlai_profile
    dsai = mlcanopy_inst.dsai_profile
    dpai = mlcanopy_inst.dpai_profile
    fracsun = mlcanopy_inst.fracsun_profile
    kb = mlcanopy_inst.kb_profile
    tb = mlcanopy_inst.tb_profile
    td = mlcanopy_inst.td_profile
    tbi = mlcanopy_inst.tbi_profile
    apar = mlcanopy_inst.apar_leaf
    swveg = mlcanopy_inst.swveg_canopy
    swvegsun = mlcanopy_inst.swvegsun_canopy
    swvegsha = mlcanopy_inst.swvegsha_canopy
    albcan = mlcanopy_inst.albcan_canopy
    swsoi = mlcanopy_inst.swsoi_soil
    swleaf = mlcanopy_inst.swleaf_leaf
    swupw = mlcanopy_inst.swupw_profile
    swdwn = mlcanopy_inst.swdwn_profile
    swbeam = mlcanopy_inst.swbeam_profile
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        chil[(p) - (bounds.begp), 0:ncan[p - 1]] = 0.0
        phi1[(p) - (bounds.begp), 0:ncan[p - 1]] = 0.0
        phi2[(p) - (bounds.begp), 0:ncan[p - 1]] = 0.0
        gdir[(p) - (bounds.begp), 0:ncan[p - 1]] = 0.0
        kb[p - 1, 0:ncan[p - 1]] = 0.0
        fracsun[p - 1, 0:ncan[p - 1]] = 0.0
        tb[p - 1, 0:ncan[p - 1]] = 0.0
        td[p - 1, 0:ncan[p - 1]] = 0.0
        tbi[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1] = 0.0
        avmu[(p) - (bounds.begp), 0:ncan[p - 1]] = 0.0
        clump_fac_ic[(p) - (bounds.begp), 0:ncan[p - 1]] = 0.0
        rho[(p) - (bounds.begp), 0:ncan[p - 1], 0:NUMRAD] = 0.0
        tau[(p) - (bounds.begp), 0:ncan[p - 1], 0:NUMRAD] = 0.0
        omega[(p) - (bounds.begp), 0:ncan[p - 1], 0:NUMRAD] = 0.0
        betab[(p) - (bounds.begp), 0:ncan[p - 1], 0:NUMRAD] = 0.0
        betad[(p) - (bounds.begp), 0:ncan[p - 1], 0:NUMRAD] = 0.0
        for ic in range(ntop[p - 1], nbot[p - 1] - 1, (-1)):
            wl = (dlai[p - 1, ic - 1] / dpai[p - 1, ic - 1])
            ws = (dsai[p - 1, ic - 1] / dpai[p - 1, ic - 1])
            for ib in range(1, NUMRAD + 1):
                if (_mlclm.leaf_optics_type == 0):
                    rho[(p) - (bounds.begp), ic - 1, ib - 1] = _f_max(((rhol[(_patchtype.patch.itype[p - 1]) - (0), ib - 1] * wl) + (rhos[(_patchtype.patch.itype[p - 1]) - (0), ib - 1] * ws)), F_1PEM06)
                    tau[(p) - (bounds.begp), ic - 1, ib - 1] = _f_max(((taul[(_patchtype.patch.itype[p - 1]) - (0), ib - 1] * wl) + (taus[(_patchtype.patch.itype[p - 1]) - (0), ib - 1] * ws)), F_1PEM06)
                elif (_mlclm.leaf_optics_type == 1):
                    raise RuntimeError('endrun')  # endrun (infra stub)
                omega[(p) - (bounds.begp), ic - 1, ib - 1] = (rho[(p) - (bounds.begp), ic - 1, ib - 1] + tau[(p) - (bounds.begp), ic - 1, ib - 1])
            if (_mlclm.leaf_optics_type == 0):
                chil[(p) - (bounds.begp), ic - 1] = xl[(_patchtype.patch.itype[p - 1]) - (0)]
            elif (_mlclm.leaf_optics_type == 1):
                raise RuntimeError('endrun')  # endrun (infra stub)
            chil[(p) - (bounds.begp), ic - 1] = _f_min(_f_max(chil[(p) - (bounds.begp), ic - 1], _mlcl.chil_min), _mlcl.chil_max)
            if (abs(chil[(p) - (bounds.begp), ic - 1]) <= F_0P01):
                chil[(p) - (bounds.begp), ic - 1] = F_0P01
            phi1[(p) - (bounds.begp), ic - 1] = ((0.5 - (F_0P633 * chil[(p) - (bounds.begp), ic - 1])) - ((F_0P330 * chil[(p) - (bounds.begp), ic - 1]) * chil[(p) - (bounds.begp), ic - 1]))
            phi2[(p) - (bounds.begp), ic - 1] = (F_0P877 * ((1.0 - (F_2P * phi1[(p) - (bounds.begp), ic - 1]))))
            gdir[(p) - (bounds.begp), ic - 1] = (phi1[(p) - (bounds.begp), ic - 1] + (phi2[(p) - (bounds.begp), ic - 1] * math.cos(solar_zen[p - 1])))
            kb[p - 1, ic - 1] = (gdir[(p) - (bounds.begp), ic - 1] / math.cos(solar_zen[p - 1]))
            kb[p - 1, ic - 1] = _f_min(kb[p - 1, ic - 1], _mlcl.kb_max)
            if (_mlclm.leaf_optics_type == 0):
                clump_fac_ic[(p) - (bounds.begp), ic - 1] = clump_fac[(_patchtype.patch.itype[p - 1]) - (0)]
            elif (_mlclm.leaf_optics_type == 1):
                raise RuntimeError('endrun')  # endrun (infra stub)
            tb[p - 1, ic - 1] = math.exp((-((kb[p - 1, ic - 1] * dpai[p - 1, ic - 1]) * clump_fac_ic[(p) - (bounds.begp), ic - 1])))
            td[p - 1, ic - 1] = 0.0
            for j in range(1, I_9 + 1):
                angle = ((((F_5P + (((j - 1)) * F_10P))) * _clm_varcon.rpi) / F_180P)
                gdirj = (phi1[(p) - (bounds.begp), ic - 1] + (phi2[(p) - (bounds.begp), ic - 1] * math.cos(angle)))
                td[p - 1, ic - 1] = (td[p - 1, ic - 1] + ((math.exp((-(((gdirj / math.cos(angle)) * dpai[p - 1, ic - 1]) * clump_fac_ic[(p) - (bounds.begp), ic - 1]))) * math.sin(angle)) * math.cos(angle)))
            td[p - 1, ic - 1] = ((td[p - 1, ic - 1] * F_2P) * (((F_10P * _clm_varcon.rpi) / F_180P)))
            if (ic == ntop[p - 1]):
                tbi[p - 1, (ic) - (0)] = 1.0
            else:
                tbi[p - 1, (ic) - (0)] = (tbi[p - 1, ((ic + 1)) - (0)] * math.exp((-((kb[p - 1, (ic + 1) - 1] * dpai[p - 1, (ic + 1) - 1]) * clump_fac_ic[(p) - (bounds.begp), (ic + 1) - 1]))))
            fracsun[p - 1, ic - 1] = ((tbi[p - 1, (ic) - (0)] / ((kb[p - 1, ic - 1] * dpai[p - 1, ic - 1]))) * ((1.0 - math.exp((-((kb[p - 1, ic - 1] * clump_fac_ic[(p) - (bounds.begp), ic - 1]) * dpai[p - 1, ic - 1]))))))
            if (fracsun[p - 1, ic - 1] <= 0.0):
                raise RuntimeError('endrun')  # endrun (infra stub)
            if (((1.0 - fracsun[p - 1, ic - 1])) <= 0.0):
                raise RuntimeError('endrun')  # endrun (infra stub)
            avmu[(p) - (bounds.begp), ic - 1] = (((1.0 - ((phi1[(p) - (bounds.begp), ic - 1] / phi2[(p) - (bounds.begp), ic - 1]) * math.log((((phi1[(p) - (bounds.begp), ic - 1] + phi2[(p) - (bounds.begp), ic - 1])) / phi1[(p) - (bounds.begp), ic - 1]))))) / phi2[(p) - (bounds.begp), ic - 1])
            for ib in range(1, NUMRAD + 1):
                betad[(p) - (bounds.begp), ic - 1, ib - 1] = ((0.5 / omega[(p) - (bounds.begp), ic - 1, ib - 1]) * (((rho[(p) - (bounds.begp), ic - 1, ib - 1] + tau[(p) - (bounds.begp), ic - 1, ib - 1]) + (((rho[(p) - (bounds.begp), ic - 1, ib - 1] - tau[(p) - (bounds.begp), ic - 1, ib - 1])) * (((((1.0 + chil[(p) - (bounds.begp), ic - 1])) / F_2P)) * ((((1.0 + chil[(p) - (bounds.begp), ic - 1])) / F_2P)))))))
                tmp0 = (gdir[(p) - (bounds.begp), ic - 1] + (phi2[(p) - (bounds.begp), ic - 1] * math.cos(solar_zen[p - 1])))
                tmp1 = (phi1[(p) - (bounds.begp), ic - 1] * math.cos(solar_zen[p - 1]))
                tmp2 = (1.0 - ((tmp1 / tmp0) * math.log((((tmp1 + tmp0)) / tmp1))))
                asu = ((((0.5 * omega[(p) - (bounds.begp), ic - 1, ib - 1]) * gdir[(p) - (bounds.begp), ic - 1]) / tmp0) * tmp2)
                betab[(p) - (bounds.begp), ic - 1, ib - 1] = ((((1.0 + (avmu[(p) - (bounds.begp), ic - 1] * kb[p - 1, ic - 1]))) / (((omega[(p) - (bounds.begp), ic - 1, ib - 1] * avmu[(p) - (bounds.begp), ic - 1]) * kb[p - 1, ic - 1]))) * asu)
        tbi[p - 1, (0) - (0)] = (tbi[p - 1, (nbot[p - 1]) - (0)] * math.exp((-((kb[p - 1, nbot[p - 1] - 1] * dpai[p - 1, nbot[p - 1] - 1]) * clump_fac_ic[(p) - (bounds.begp), nbot[p - 1] - 1]))))
    if (_mlclm.light_type == 1):
        mlcanopy_inst = norman(bounds, num_filter, filter, rho, tau, omega, mlcanopy_inst)
    elif (_mlclm.light_type == 2):
        mlcanopy_inst = twostream(bounds, num_filter, filter, omega, avmu, betad, betab, clump_fac_ic, mlcanopy_inst)
    else:
        raise RuntimeError('endrun')  # endrun (infra stub)
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            apar[p - 1, ic - 1, ISUN - 1] = (swleaf[p - 1, ic - 1, ISUN - 1, IVIS - 1] * _mlcl.j_to_umol)
            apar[p - 1, ic - 1, ISHA - 1] = (swleaf[p - 1, ic - 1, ISHA - 1, IVIS - 1] * _mlcl.j_to_umol)
    return mlcanopy_inst

def norman(bounds, num_filter, filter, rho, tau, omega, mlcanopy_inst):
    """L292-L577 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    neq = (NLEVMLCAN + 1) * 2
    fp = 0
    p = 0
    ic = 0
    icm1 = 0
    ib = 0
    suminc = 0.0
    sumref = 0.0
    sumabs = 0.0
    err = 0.0
    refld = 0.0
    trand = 0.0
    m = 0
    aic = 0.0
    bic = 0.0
    eic = 0.0
    fic = 0.0
    atri = np.empty((neq,), dtype=np.float64)
    btri = np.empty((neq,), dtype=np.float64)
    ctri = np.empty((neq,), dtype=np.float64)
    dtri = np.empty((neq,), dtype=np.float64)
    utri = np.empty((neq,), dtype=np.float64)
    swabsb = 0.0
    swabsd = 0.0
    swsun = 0.0
    swsha = 0.0
    # B001 <- L337-L576
    swskyb = mlcanopy_inst.swskyb_forcing
    swskyd = mlcanopy_inst.swskyd_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    nbot = mlcanopy_inst.nbot_canopy
    albsoib = mlcanopy_inst.albsoib_soil
    albsoid = mlcanopy_inst.albsoid_soil
    dpai = mlcanopy_inst.dpai_profile
    fracsun = mlcanopy_inst.fracsun_profile
    tb = mlcanopy_inst.tb_profile
    td = mlcanopy_inst.td_profile
    tbi = mlcanopy_inst.tbi_profile
    swveg = mlcanopy_inst.swveg_canopy
    swvegsun = mlcanopy_inst.swvegsun_canopy
    swvegsha = mlcanopy_inst.swvegsha_canopy
    albcan = mlcanopy_inst.albcan_canopy
    swsoi = mlcanopy_inst.swsoi_soil
    swleaf = mlcanopy_inst.swleaf_leaf
    swupw = mlcanopy_inst.swupw_profile
    swdwn = mlcanopy_inst.swdwn_profile
    swbeam = mlcanopy_inst.swbeam_profile
    for ib in range(1, NUMRAD + 1):
        for fp in range(1, num_filter + 1):
            p = filter[fp - 1]
            swbeam[p - 1, (0) - (0), ib - 1] = 0.0
            swupw[p - 1, (0) - (0), ib - 1] = 0.0
            swdwn[p - 1, (0) - (0), ib - 1] = 0.0
            for ic in range(1, ncan[p - 1] + 1):
                swbeam[p - 1, (ic) - (0), ib - 1] = 0.0
                swupw[p - 1, (ic) - (0), ib - 1] = 0.0
                swdwn[p - 1, (ic) - (0), ib - 1] = 0.0
                swleaf[p - 1, ic - 1, ISUN - 1, ib - 1] = 0.0
                swleaf[p - 1, ic - 1, ISHA - 1, ib - 1] = 0.0
            m = 0
            m = (m + 1)
            atri[m - 1] = 0.0
            btri[m - 1] = 1.0
            ctri[m - 1] = (-albsoid[p - 1, ib - 1])
            dtri[m - 1] = ((swskyb[p - 1, ib - 1] * tbi[p - 1, (0) - (0)]) * albsoib[p - 1, ib - 1])
            refld = (((1.0 - td[p - 1, nbot[p - 1] - 1])) * rho[(p) - (bounds.begp), nbot[p - 1] - 1, ib - 1])
            trand = ((((1.0 - td[p - 1, nbot[p - 1] - 1])) * tau[(p) - (bounds.begp), nbot[p - 1] - 1, ib - 1]) + td[p - 1, nbot[p - 1] - 1])
            aic = (refld - ((trand * trand) / refld))
            bic = (trand / refld)
            m = (m + 1)
            atri[m - 1] = (-aic)
            btri[m - 1] = 1.0
            ctri[m - 1] = (-bic)
            dtri[m - 1] = (((swskyb[p - 1, ib - 1] * tbi[p - 1, (nbot[p - 1]) - (0)]) * ((1.0 - tb[p - 1, nbot[p - 1] - 1]))) * ((tau[(p) - (bounds.begp), nbot[p - 1] - 1, ib - 1] - (rho[(p) - (bounds.begp), nbot[p - 1] - 1, ib - 1] * bic))))
            for ic in range(nbot[p - 1], (ntop[p - 1] - 1) + 1):
                refld = (((1.0 - td[p - 1, ic - 1])) * rho[(p) - (bounds.begp), ic - 1, ib - 1])
                trand = ((((1.0 - td[p - 1, ic - 1])) * tau[(p) - (bounds.begp), ic - 1, ib - 1]) + td[p - 1, ic - 1])
                fic = (refld - ((trand * trand) / refld))
                eic = (trand / refld)
                m = (m + 1)
                atri[m - 1] = (-eic)
                btri[m - 1] = 1.0
                ctri[m - 1] = (-fic)
                dtri[m - 1] = (((swskyb[p - 1, ib - 1] * tbi[p - 1, (ic) - (0)]) * ((1.0 - tb[p - 1, ic - 1]))) * ((rho[(p) - (bounds.begp), ic - 1, ib - 1] - (tau[(p) - (bounds.begp), ic - 1, ib - 1] * eic))))
                refld = (((1.0 - td[p - 1, (ic + 1) - 1])) * rho[(p) - (bounds.begp), (ic + 1) - 1, ib - 1])
                trand = ((((1.0 - td[p - 1, (ic + 1) - 1])) * tau[(p) - (bounds.begp), (ic + 1) - 1, ib - 1]) + td[p - 1, (ic + 1) - 1])
                aic = (refld - ((trand * trand) / refld))
                bic = (trand / refld)
                m = (m + 1)
                atri[m - 1] = (-aic)
                btri[m - 1] = 1.0
                ctri[m - 1] = (-bic)
                dtri[m - 1] = (((swskyb[p - 1, ib - 1] * tbi[p - 1, ((ic + 1)) - (0)]) * ((1.0 - tb[p - 1, (ic + 1) - 1]))) * ((tau[(p) - (bounds.begp), (ic + 1) - 1, ib - 1] - (rho[(p) - (bounds.begp), (ic + 1) - 1, ib - 1] * bic))))
            ic = int(ntop[p - 1])
            refld = (((1.0 - td[p - 1, ic - 1])) * rho[(p) - (bounds.begp), ic - 1, ib - 1])
            trand = ((((1.0 - td[p - 1, ic - 1])) * tau[(p) - (bounds.begp), ic - 1, ib - 1]) + td[p - 1, ic - 1])
            fic = (refld - ((trand * trand) / refld))
            eic = (trand / refld)
            m = (m + 1)
            atri[m - 1] = (-eic)
            btri[m - 1] = 1.0
            ctri[m - 1] = (-fic)
            dtri[m - 1] = (((swskyb[p - 1, ib - 1] * tbi[p - 1, (ic) - (0)]) * ((1.0 - tb[p - 1, ic - 1]))) * ((rho[(p) - (bounds.begp), ic - 1, ib - 1] - (tau[(p) - (bounds.begp), ic - 1, ib - 1] * eic))))
            m = (m + 1)
            atri[m - 1] = 0.0
            btri[m - 1] = 1.0
            ctri[m - 1] = 0.0
            dtri[m - 1] = swskyd[p - 1, ib - 1]
            _f_copy_out(utri, _mlm.tridiag(atri, btri, ctri, dtri, utri, m))
            m = 0
            m = (m + 1)
            swupw[p - 1, (0) - (0), ib - 1] = utri[m - 1]
            m = (m + 1)
            swdwn[p - 1, (0) - (0), ib - 1] = utri[m - 1]
            for ic in range(nbot[p - 1], ntop[p - 1] + 1):
                m = (m + 1)
                swupw[p - 1, (ic) - (0), ib - 1] = utri[m - 1]
                m = (m + 1)
                swdwn[p - 1, (ic) - (0), ib - 1] = utri[m - 1]
    for ib in range(1, NUMRAD + 1):
        for fp in range(1, num_filter + 1):
            p = filter[fp - 1]
            swbeam[p - 1, (0) - (0), ib - 1] = (tbi[p - 1, (0) - (0)] * swskyb[p - 1, ib - 1])
            swabsb = (swbeam[p - 1, (0) - (0), ib - 1] * ((1.0 - albsoib[p - 1, ib - 1])))
            swabsd = (swdwn[p - 1, (0) - (0), ib - 1] * ((1.0 - albsoid[p - 1, ib - 1])))
            swsoi[p - 1, ib - 1] = (swabsb + swabsd)
            swveg[p - 1, ib - 1] = 0.0
            swvegsun[p - 1, ib - 1] = 0.0
            swvegsha[p - 1, ib - 1] = 0.0
            for ic in range(nbot[p - 1], ntop[p - 1] + 1):
                swbeam[p - 1, (ic) - (0), ib - 1] = (tbi[p - 1, (ic) - (0)] * swskyb[p - 1, ib - 1])
                swabsb = ((swbeam[p - 1, (ic) - (0), ib - 1] * ((1.0 - tb[p - 1, ic - 1]))) * ((1.0 - omega[(p) - (bounds.begp), ic - 1, ib - 1])))
                if (ic == nbot[p - 1]):
                    icm1 = 0
                else:
                    icm1 = (ic - 1)
                swabsd = ((((swdwn[p - 1, (ic) - (0), ib - 1] + swupw[p - 1, (icm1) - (0), ib - 1])) * ((1.0 - td[p - 1, ic - 1]))) * ((1.0 - omega[(p) - (bounds.begp), ic - 1, ib - 1])))
                swsha = (swabsd * ((1.0 - fracsun[p - 1, ic - 1])))
                swsun = ((swabsd * fracsun[p - 1, ic - 1]) + swabsb)
                swleaf[p - 1, ic - 1, ISUN - 1, ib - 1] = (swsun / ((fracsun[p - 1, ic - 1] * dpai[p - 1, ic - 1])))
                swleaf[p - 1, ic - 1, ISHA - 1, ib - 1] = (swsha / ((((1.0 - fracsun[p - 1, ic - 1])) * dpai[p - 1, ic - 1])))
                swveg[p - 1, ib - 1] = (swveg[p - 1, ib - 1] + ((swabsb + swabsd)))
                swvegsun[p - 1, ib - 1] = (swvegsun[p - 1, ib - 1] + swsun)
                swvegsha[p - 1, ib - 1] = (swvegsha[p - 1, ib - 1] + swsha)
            suminc = (swskyb[p - 1, ib - 1] + swskyd[p - 1, ib - 1])
            if (suminc > 0.0):
                albcan[p - 1, ib - 1] = (swupw[p - 1, (ntop[p - 1]) - (0), ib - 1] / suminc)
            else:
                albcan[p - 1, ib - 1] = 0.0
            sumref = (albcan[p - 1, ib - 1] * ((swskyb[p - 1, ib - 1] + swskyd[p - 1, ib - 1])))
            sumabs = (suminc - sumref)
            err = (sumabs - ((swveg[p - 1, ib - 1] + swsoi[p - 1, ib - 1])))
            if (abs(err) > F_1PEM03):
                raise RuntimeError('endrun')  # endrun (infra stub)
            err = (((swvegsun[p - 1, ib - 1] + swvegsha[p - 1, ib - 1])) - swveg[p - 1, ib - 1])
            if (abs(err) > F_1PEM03):
                raise RuntimeError('endrun')  # endrun (infra stub)
    return mlcanopy_inst

def twostream(bounds, num_filter, filter, omega, avmu, betad, betab, clump_fac_ic, mlcanopy_inst):
    """L580-L877 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    unitb = np.float64('1.')
    unitd = np.float64('1.')
    fp = 0
    p = 0
    ib = 0
    ic = 0
    b = 0.0
    c = 0.0
    d = 0.0
    h = 0.0
    u = 0.0
    v = 0.0
    g1 = 0.0
    g2 = 0.0
    s1 = 0.0
    s2 = 0.0
    num1 = 0.0
    num2 = 0.0
    den1 = 0.0
    den2 = 0.0
    n1b = 0.0
    n2b = 0.0
    n1d = 0.0
    n2d = 0.0
    a1b = 0.0
    a2b = 0.0
    a1d = 0.0
    a2d = 0.0
    dir = 0.0
    dif = 0.0
    sun = 0.0
    sha = 0.0
    suminc = 0.0
    sumref = 0.0
    sumabs = 0.0
    iupwb0 = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iupwb = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    idwnb = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsb = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsbb = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsbs = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsb_sun = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsb_sha = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iupwd0 = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iupwd = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    idwnd = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsd = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsd_sun = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    iabsd_sha = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NUMRAD,), dtype=np.float64)
    albb_below = np.empty(((bounds.endp) - (bounds.begp) + 1, NUMRAD,), dtype=np.float64)
    albd_below = np.empty(((bounds.endp) - (bounds.begp) + 1, NUMRAD,), dtype=np.float64)
    # B001 <- L646-L876
    swskyb = mlcanopy_inst.swskyb_forcing
    swskyd = mlcanopy_inst.swskyd_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    nbot = mlcanopy_inst.nbot_canopy
    albsoib = mlcanopy_inst.albsoib_soil
    albsoid = mlcanopy_inst.albsoid_soil
    dpai = mlcanopy_inst.dpai_profile
    fracsun = mlcanopy_inst.fracsun_profile
    kb = mlcanopy_inst.kb_profile
    tbi = mlcanopy_inst.tbi_profile
    swveg = mlcanopy_inst.swveg_canopy
    swvegsun = mlcanopy_inst.swvegsun_canopy
    swvegsha = mlcanopy_inst.swvegsha_canopy
    albcan = mlcanopy_inst.albcan_canopy
    swsoi = mlcanopy_inst.swsoi_soil
    swleaf = mlcanopy_inst.swleaf_leaf
    swupw = mlcanopy_inst.swupw_profile
    swdwn = mlcanopy_inst.swdwn_profile
    swbeam = mlcanopy_inst.swbeam_profile
    for ib in range(1, NUMRAD + 1):
        for fp in range(1, num_filter + 1):
            p = filter[fp - 1]
            swbeam[p - 1, (0) - (0), ib - 1] = 0.0
            swupw[p - 1, (0) - (0), ib - 1] = 0.0
            swdwn[p - 1, (0) - (0), ib - 1] = 0.0
            for ic in range(1, ncan[p - 1] + 1):
                swbeam[p - 1, (ic) - (0), ib - 1] = 0.0
                swupw[p - 1, (ic) - (0), ib - 1] = 0.0
                swdwn[p - 1, (ic) - (0), ib - 1] = 0.0
                swleaf[p - 1, ic - 1, ISUN - 1, ib - 1] = 0.0
                swleaf[p - 1, ic - 1, ISHA - 1, ib - 1] = 0.0
    for ib in range(1, NUMRAD + 1):
        for fp in range(1, num_filter + 1):
            p = filter[fp - 1]
            albb_below[(p) - (bounds.begp), ib - 1] = albsoib[p - 1, ib - 1]
            albd_below[(p) - (bounds.begp), ib - 1] = albsoid[p - 1, ib - 1]
            for ic in range(nbot[p - 1], ntop[p - 1] + 1):
                b = (((1.0 - (((1.0 - betad[(p) - (bounds.begp), ic - 1, ib - 1])) * omega[(p) - (bounds.begp), ic - 1, ib - 1]))) / avmu[(p) - (bounds.begp), ic - 1])
                c = ((betad[(p) - (bounds.begp), ic - 1, ib - 1] * omega[(p) - (bounds.begp), ic - 1, ib - 1]) / avmu[(p) - (bounds.begp), ic - 1])
                h = math.sqrt(((b * b) - (c * c)))
                u = ((((h - b) - c)) / ((F_2P * h)))
                v = ((((h + b) + c)) / ((F_2P * h)))
                d = (((omega[(p) - (bounds.begp), ic - 1, ib - 1] * kb[p - 1, ic - 1]) * unitb) / (((h * h) - (kb[p - 1, ic - 1] * kb[p - 1, ic - 1]))))
                g1 = (((((betab[(p) - (bounds.begp), ic - 1, ib - 1] * kb[p - 1, ic - 1]) - (b * betab[(p) - (bounds.begp), ic - 1, ib - 1])) - (c * ((1.0 - betab[(p) - (bounds.begp), ic - 1, ib - 1]))))) * d)
                g2 = (((((((1.0 - betab[(p) - (bounds.begp), ic - 1, ib - 1])) * kb[p - 1, ic - 1]) + (c * betab[(p) - (bounds.begp), ic - 1, ib - 1])) + (b * ((1.0 - betab[(p) - (bounds.begp), ic - 1, ib - 1]))))) * d)
                s1 = math.exp((-((h * clump_fac_ic[(p) - (bounds.begp), ic - 1]) * dpai[p - 1, ic - 1])))
                s2 = math.exp((-((kb[p - 1, ic - 1] * clump_fac_ic[(p) - (bounds.begp), ic - 1]) * dpai[p - 1, ic - 1])))
                num1 = ((v * (((g1 + (g2 * albd_below[(p) - (bounds.begp), ib - 1])) + (albb_below[(p) - (bounds.begp), ib - 1] * unitb)))) * s2)
                num2 = ((g2 * ((u + (v * albd_below[(p) - (bounds.begp), ib - 1])))) * s1)
                den1 = ((v * ((v + (u * albd_below[(p) - (bounds.begp), ib - 1])))) / s1)
                den2 = ((u * ((u + (v * albd_below[(p) - (bounds.begp), ib - 1])))) * s1)
                n2b = (((num1 - num2)) / ((den1 - den2)))
                n1b = (((g2 - (n2b * u))) / v)
                a1b = (((-((g1 * ((1.0 - (s2 * s2)))) / ((F_2P * kb[p - 1, ic - 1])))) + (((n1b * u) * ((1.0 - (s2 * s1)))) / ((kb[p - 1, ic - 1] + h)))) + (((n2b * v) * ((1.0 - (s2 / s1)))) / ((kb[p - 1, ic - 1] - h))))
                a2b = ((((g2 * ((1.0 - (s2 * s2)))) / ((F_2P * kb[p - 1, ic - 1]))) - (((n1b * v) * ((1.0 - (s2 * s1)))) / ((kb[p - 1, ic - 1] + h)))) - (((n2b * u) * ((1.0 - (s2 / s1)))) / ((kb[p - 1, ic - 1] - h))))
                a1b = (a1b * tbi[p - 1, (ic) - (0)])
                a2b = (a2b * tbi[p - 1, (ic) - (0)])
                iupwb0[(p) - (bounds.begp), ic - 1, ib - 1] = (((-g1) + (n1b * u)) + (n2b * v))
                iupwb[(p) - (bounds.begp), ic - 1, ib - 1] = (((-(g1 * s2)) + ((n1b * u) * s1)) + ((n2b * v) / s1))
                idwnb[(p) - (bounds.begp), ic - 1, ib - 1] = (((g2 * s2) - ((n1b * v) * s1)) - ((n2b * u) / s1))
                iabsb[(p) - (bounds.begp), ic - 1, ib - 1] = ((((unitb * ((1.0 - s2))) - iupwb0[(p) - (bounds.begp), ic - 1, ib - 1]) + iupwb[(p) - (bounds.begp), ic - 1, ib - 1]) - idwnb[(p) - (bounds.begp), ic - 1, ib - 1])
                iabsbb[(p) - (bounds.begp), ic - 1, ib - 1] = ((((1.0 - omega[(p) - (bounds.begp), ic - 1, ib - 1])) * unitb) * ((1.0 - s2)))
                iabsbs[(p) - (bounds.begp), ic - 1, ib - 1] = (((((omega[(p) - (bounds.begp), ic - 1, ib - 1] * unitb) * ((1.0 - s2))) - iupwb0[(p) - (bounds.begp), ic - 1, ib - 1]) + iupwb[(p) - (bounds.begp), ic - 1, ib - 1]) - idwnb[(p) - (bounds.begp), ic - 1, ib - 1])
                iabsb_sun[(p) - (bounds.begp), ic - 1, ib - 1] = (((1.0 - omega[(p) - (bounds.begp), ic - 1, ib - 1])) * (((((1.0 - s2)) * unitb) + ((clump_fac_ic[(p) - (bounds.begp), ic - 1] / avmu[(p) - (bounds.begp), ic - 1]) * ((a1b + a2b))))))
                iabsb_sha[(p) - (bounds.begp), ic - 1, ib - 1] = (iabsb[(p) - (bounds.begp), ic - 1, ib - 1] - iabsb_sun[(p) - (bounds.begp), ic - 1, ib - 1])
                num1 = ((unitd * ((u + (v * albd_below[(p) - (bounds.begp), ib - 1])))) * s1)
                den1 = ((v * ((v + (u * albd_below[(p) - (bounds.begp), ib - 1])))) / s1)
                den2 = ((u * ((u + (v * albd_below[(p) - (bounds.begp), ib - 1])))) * s1)
                n2d = (num1 / ((den1 - den2)))
                n1d = (-(((unitd + (n2d * u))) / v))
                a1d = ((((n1d * u) * ((1.0 - (s2 * s1)))) / ((kb[p - 1, ic - 1] + h))) + (((n2d * v) * ((1.0 - (s2 / s1)))) / ((kb[p - 1, ic - 1] - h))))
                a2d = ((-(((n1d * v) * ((1.0 - (s2 * s1)))) / ((kb[p - 1, ic - 1] + h)))) - (((n2d * u) * ((1.0 - (s2 / s1)))) / ((kb[p - 1, ic - 1] - h))))
                a1d = (a1d * tbi[p - 1, (ic) - (0)])
                a2d = (a2d * tbi[p - 1, (ic) - (0)])
                iupwd0[(p) - (bounds.begp), ic - 1, ib - 1] = ((n1d * u) + (n2d * v))
                iupwd[(p) - (bounds.begp), ic - 1, ib - 1] = (((n1d * u) * s1) + ((n2d * v) / s1))
                idwnd[(p) - (bounds.begp), ic - 1, ib - 1] = ((-((n1d * v) * s1)) - ((n2d * u) / s1))
                iabsd[(p) - (bounds.begp), ic - 1, ib - 1] = (((unitd - iupwd0[(p) - (bounds.begp), ic - 1, ib - 1]) + iupwd[(p) - (bounds.begp), ic - 1, ib - 1]) - idwnd[(p) - (bounds.begp), ic - 1, ib - 1])
                iabsd_sun[(p) - (bounds.begp), ic - 1, ib - 1] = (((((1.0 - omega[(p) - (bounds.begp), ic - 1, ib - 1])) * clump_fac_ic[(p) - (bounds.begp), ic - 1]) / avmu[(p) - (bounds.begp), ic - 1]) * ((a1d + a2d)))
                iabsd_sha[(p) - (bounds.begp), ic - 1, ib - 1] = (iabsd[(p) - (bounds.begp), ic - 1, ib - 1] - iabsd_sun[(p) - (bounds.begp), ic - 1, ib - 1])
                albb_below[(p) - (bounds.begp), ib - 1] = iupwb0[(p) - (bounds.begp), ic - 1, ib - 1]
                albd_below[(p) - (bounds.begp), ib - 1] = iupwd0[(p) - (bounds.begp), ic - 1, ib - 1]
            dir = swskyb[p - 1, ib - 1]
            dif = swskyd[p - 1, ib - 1]
            for ic in range(ntop[p - 1], nbot[p - 1] - 1, (-1)):
                swbeam[p - 1, (ic) - (0), ib - 1] = dir
                swdwn[p - 1, (ic) - (0), ib - 1] = dif
                swupw[p - 1, (ic) - (0), ib - 1] = ((iupwd0[(p) - (bounds.begp), ic - 1, ib - 1] * dif) + (iupwb0[(p) - (bounds.begp), ic - 1, ib - 1] * dir))
                sun = ((((iabsb_sun[(p) - (bounds.begp), ic - 1, ib - 1] * dir) + (iabsd_sun[(p) - (bounds.begp), ic - 1, ib - 1] * dif))) / ((fracsun[p - 1, ic - 1] * dpai[p - 1, ic - 1])))
                sha = ((((iabsb_sha[(p) - (bounds.begp), ic - 1, ib - 1] * dir) + (iabsd_sha[(p) - (bounds.begp), ic - 1, ib - 1] * dif))) / ((((1.0 - fracsun[p - 1, ic - 1])) * dpai[p - 1, ic - 1])))
                swleaf[p - 1, ic - 1, ISUN - 1, ib - 1] = sun
                swleaf[p - 1, ic - 1, ISHA - 1, ib - 1] = sha
                dif = ((dir * idwnb[(p) - (bounds.begp), ic - 1, ib - 1]) + (dif * idwnd[(p) - (bounds.begp), ic - 1, ib - 1]))
                dir = (dir * math.exp((-((kb[p - 1, ic - 1] * clump_fac_ic[(p) - (bounds.begp), ic - 1]) * dpai[p - 1, ic - 1]))))
            swbeam[p - 1, (0) - (0), ib - 1] = dir
            swdwn[p - 1, (0) - (0), ib - 1] = dif
            swupw[p - 1, (0) - (0), ib - 1] = ((albsoid[p - 1, ib - 1] * dif) + (albsoib[p - 1, ib - 1] * dir))
            swsoi[p - 1, ib - 1] = ((dir * ((1.0 - albsoib[p - 1, ib - 1]))) + (dif * ((1.0 - albsoid[p - 1, ib - 1]))))
            suminc = (swskyb[p - 1, ib - 1] + swskyd[p - 1, ib - 1])
            sumref = ((iupwb0[(p) - (bounds.begp), ntop[p - 1] - 1, ib - 1] * swskyb[p - 1, ib - 1]) + (iupwd0[(p) - (bounds.begp), ntop[p - 1] - 1, ib - 1] * swskyd[p - 1, ib - 1]))
            if (suminc > 0.0):
                albcan[p - 1, ib - 1] = (sumref / suminc)
            else:
                albcan[p - 1, ib - 1] = 0.0
            swveg[p - 1, ib - 1] = 0.0
            swvegsun[p - 1, ib - 1] = 0.0
            swvegsha[p - 1, ib - 1] = 0.0
            for ic in range(nbot[p - 1], ntop[p - 1] + 1):
                sun = ((swleaf[p - 1, ic - 1, ISUN - 1, ib - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1])
                sha = ((swleaf[p - 1, ic - 1, ISHA - 1, ib - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1])
                swveg[p - 1, ib - 1] = (swveg[p - 1, ib - 1] + ((sun + sha)))
                swvegsun[p - 1, ib - 1] = (swvegsun[p - 1, ib - 1] + sun)
                swvegsha[p - 1, ib - 1] = (swvegsha[p - 1, ib - 1] + sha)
            suminc = (swskyb[p - 1, ib - 1] + swskyd[p - 1, ib - 1])
            sumref = (albcan[p - 1, ib - 1] * suminc)
            sumabs = (swveg[p - 1, ib - 1] + swsoi[p - 1, ib - 1])
            if (abs((suminc - ((sumabs + sumref)))) >= F_1PEM06):
                raise RuntimeError('endrun')  # endrun (infra stub)
    return mlcanopy_inst


# Flattened adapters for the differential gate (recast.transform.numpy.flat).
class _Record:
    def __init__(self, **fields):
        self.__dict__.update(fields)

def solarradiation_flat(num_filter, filter, np_, bounds__begp, bounds__endp, mlcanopy_inst__albcan_canopy, mlcanopy_inst__albsoib_soil, mlcanopy_inst__albsoid_soil, mlcanopy_inst__apar_leaf, mlcanopy_inst__dlai_profile, mlcanopy_inst__dpai_profile, mlcanopy_inst__dsai_profile, mlcanopy_inst__fracsun_profile, mlcanopy_inst__kb_profile, mlcanopy_inst__nbot_canopy, mlcanopy_inst__ncan_canopy, mlcanopy_inst__ntop_canopy, mlcanopy_inst__solar_zen_forcing, mlcanopy_inst__swbeam_profile, mlcanopy_inst__swdwn_profile, mlcanopy_inst__swleaf_leaf, mlcanopy_inst__swskyb_forcing, mlcanopy_inst__swskyd_forcing, mlcanopy_inst__swsoi_soil, mlcanopy_inst__swupw_profile, mlcanopy_inst__swveg_canopy, mlcanopy_inst__swvegsha_canopy, mlcanopy_inst__swvegsun_canopy, mlcanopy_inst__tb_profile, mlcanopy_inst__tbi_profile, mlcanopy_inst__td_profile, mlpftcon__clump_fac, patch__itype, pftcon__rhol, pftcon__rhos, pftcon__taul, pftcon__taus, pftcon__xl, mlclm_varcon__chil_max, mlclm_varcon__chil_min, mlclm_varcon__j_to_umol, mlclm_varcon__kb_max, mlclm_varctl__leaf_optics_type, mlclm_varctl__light_type):
    bounds = _Record(begp=bounds__begp, endp=bounds__endp)
    mlcanopy_inst = _Record(albcan_canopy=mlcanopy_inst__albcan_canopy, albsoib_soil=mlcanopy_inst__albsoib_soil, albsoid_soil=mlcanopy_inst__albsoid_soil, apar_leaf=mlcanopy_inst__apar_leaf, dlai_profile=mlcanopy_inst__dlai_profile, dpai_profile=mlcanopy_inst__dpai_profile, dsai_profile=mlcanopy_inst__dsai_profile, fracsun_profile=mlcanopy_inst__fracsun_profile, kb_profile=mlcanopy_inst__kb_profile, nbot_canopy=mlcanopy_inst__nbot_canopy, ncan_canopy=mlcanopy_inst__ncan_canopy, ntop_canopy=mlcanopy_inst__ntop_canopy, solar_zen_forcing=mlcanopy_inst__solar_zen_forcing, swbeam_profile=mlcanopy_inst__swbeam_profile, swdwn_profile=mlcanopy_inst__swdwn_profile, swleaf_leaf=mlcanopy_inst__swleaf_leaf, swskyb_forcing=mlcanopy_inst__swskyb_forcing, swskyd_forcing=mlcanopy_inst__swskyd_forcing, swsoi_soil=mlcanopy_inst__swsoi_soil, swupw_profile=mlcanopy_inst__swupw_profile, swveg_canopy=mlcanopy_inst__swveg_canopy, swvegsha_canopy=mlcanopy_inst__swvegsha_canopy, swvegsun_canopy=mlcanopy_inst__swvegsun_canopy, tb_profile=mlcanopy_inst__tb_profile, tbi_profile=mlcanopy_inst__tbi_profile, td_profile=mlcanopy_inst__td_profile)
    import mlpftconmod_numpy as _mlpftconmod
    if not hasattr(getattr(_mlpftconmod, 'mlpftcon', None), '__dict__'):
        _mlpftconmod.mlpftcon = _Record()
    _mlpftconmod.mlpftcon.clump_fac = mlpftcon__clump_fac
    import patchtype_numpy as _patchtype
    if not hasattr(getattr(_patchtype, 'patch', None), '__dict__'):
        _patchtype.patch = _Record()
    _patchtype.patch.itype = patch__itype
    import pftconmod_numpy as _pftconmod
    if not hasattr(getattr(_pftconmod, 'pftcon', None), '__dict__'):
        _pftconmod.pftcon = _Record()
    _pftconmod.pftcon.rhol = pftcon__rhol
    _pftconmod.pftcon.rhos = pftcon__rhos
    _pftconmod.pftcon.taul = pftcon__taul
    _pftconmod.pftcon.taus = pftcon__taus
    _pftconmod.pftcon.xl = pftcon__xl
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.chil_max = mlclm_varcon__chil_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.chil_min = mlclm_varcon__chil_min
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.j_to_umol = mlclm_varcon__j_to_umol
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.kb_max = mlclm_varcon__kb_max
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.leaf_optics_type = mlclm_varctl__leaf_optics_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.light_type = mlclm_varctl__light_type
    _out = solarradiation(bounds=bounds, num_filter=num_filter, filter=filter, mlcanopy_inst=mlcanopy_inst)
    _out = (_out,)
    mlcanopy_inst_, = _out
    mlcanopy_inst__albcan_canopy = mlcanopy_inst.albcan_canopy
    mlcanopy_inst__apar_leaf = mlcanopy_inst.apar_leaf
    mlcanopy_inst__fracsun_profile = mlcanopy_inst.fracsun_profile
    mlcanopy_inst__kb_profile = mlcanopy_inst.kb_profile
    mlcanopy_inst__swbeam_profile = mlcanopy_inst.swbeam_profile
    mlcanopy_inst__swdwn_profile = mlcanopy_inst.swdwn_profile
    mlcanopy_inst__swleaf_leaf = mlcanopy_inst.swleaf_leaf
    mlcanopy_inst__swsoi_soil = mlcanopy_inst.swsoi_soil
    mlcanopy_inst__swupw_profile = mlcanopy_inst.swupw_profile
    mlcanopy_inst__swveg_canopy = mlcanopy_inst.swveg_canopy
    mlcanopy_inst__swvegsha_canopy = mlcanopy_inst.swvegsha_canopy
    mlcanopy_inst__swvegsun_canopy = mlcanopy_inst.swvegsun_canopy
    mlcanopy_inst__tb_profile = mlcanopy_inst.tb_profile
    mlcanopy_inst__tbi_profile = mlcanopy_inst.tbi_profile
    mlcanopy_inst__td_profile = mlcanopy_inst.td_profile
    return mlcanopy_inst__albcan_canopy, mlcanopy_inst__apar_leaf, mlcanopy_inst__fracsun_profile, mlcanopy_inst__kb_profile, mlcanopy_inst__swbeam_profile, mlcanopy_inst__swdwn_profile, mlcanopy_inst__swleaf_leaf, mlcanopy_inst__swsoi_soil, mlcanopy_inst__swupw_profile, mlcanopy_inst__swveg_canopy, mlcanopy_inst__swvegsha_canopy, mlcanopy_inst__swvegsun_canopy, mlcanopy_inst__tb_profile, mlcanopy_inst__tbi_profile, mlcanopy_inst__td_profile

_SIGNATURES.update({
    'solarradiation_flat': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'num_filter'}]}, {'name': 'np_', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'bounds__begp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}, {'name': 'bounds__endp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}, {'name': 'mlcanopy_inst__albcan_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__albsoib_soil', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__albsoid_soil', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__apar_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__dlai_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__dpai_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__dsai_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__fracsun_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__kb_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__nbot_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ncan_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ntop_canopy', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__solar_zen_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__swbeam_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swdwn_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyb_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyd_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swupw_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__tb_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__tbi_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}]}, {'name': 'mlcanopy_inst__td_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlpftcon__clump_fac', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'patch__itype', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'pftcon__rhol', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__rhos', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__taul', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__taus', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__xl', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlclm_varcon__chil_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__chil_min', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__j_to_umol', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__kb_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__leaf_optics_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__light_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}], 'result': None, 'result_dtype': None},
})
