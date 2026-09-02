"""Machine-translated from MLCanopyFluxesMod.f90 by recast.

NumPy/scalar direct translation. Module state mirrors the Fortran
module exactly; call mlcanopyfluxes before use.
DO NOT hand-edit mechanical blocks -- fix the engine instead.
"""

import math
import os
import re as _re
from typing import Any

import numpy as np

from mlcanopyfluxesmod_constants import *  # noqa: F401,F403
from mlcanopyfluxesmod_use_constants import *  # noqa: F401,F403
import atm2lndtype_numpy as _atm
import canopystatetype_numpy as _can
import clm_time_manager_numpy as _clm
import clm_varcon_numpy as _clm_varcon
import clm_varorb_numpy as _clm_varorb
import clm_varpar_numpy as _clm_varpar
import columntype_numpy as _columntype
import energyfluxtype_numpy as _ene
import frictionvelocitymod_numpy as _fri
import gridcelltype_numpy as _gri
import mlcanopyfluxestype_numpy as _mlc
import mlcanopynitrogenprofilemod_numpy as _mlca
import mlcanopyturbulencemod_numpy as _mlcan
import mlcanopywatermod_numpy as _mlcano
import mlclm_varcon_numpy as _mlcl
import mlclm_varctl_numpy as _mlclm
import mlfluxprofilesolutionmod_numpy as _mlf
import mlgetatmforcingmod_numpy as _mlg
import mlinitverticalmod_numpy as _mli
import mlleafboundarylayermod_numpy as _mll
import mlleafheatcapacitymod_numpy as _mlle
import mlleafphotosynthesismod_numpy as _mllea
import mllongwaveradiationmod_numpy as _mllo
import mlplanthydraulicsmod_numpy as _mlp
import mlrungekuttamod_numpy as _mlr
import mlsolarradiationmod_numpy as _mls
import mlwatervapormod_numpy as _mlw
import patchtype_numpy as _patchtype
import shr_orb_mod_numpy as _shr
import soilstatetype_numpy as _soi
import solarabsorbedtype_numpy as _sol
import spmdmod_numpy as _spmdmod
import surfacealbedotype_numpy as _sur
import temperaturetype_numpy as _tem
import wateratm2lndbulktype_numpy as _wat
import waterdiagnosticbulktype_numpy as _wate
import waterfluxbulktype_numpy as _water
import waterstatebulktype_numpy as _waters

_RUNTIME = {'abort_msg': None}

_SIGNATURES = {'mlcanopyfluxes': {'kind': 'subroutine', 'args': [{'name': 'bounds', 'dtype': 'UNKNOWN(TYPE(BOUNDS_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'num_exposedvegp', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter_exposedvegp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'atm2lnd_inst', 'dtype': 'UNKNOWN(TYPE(ATM2LND_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'canopystate_inst', 'dtype': 'UNKNOWN(TYPE(CANOPYSTATE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'soilstate_inst', 'dtype': 'UNKNOWN(TYPE(SOILSTATE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'temperature_inst', 'dtype': 'UNKNOWN(TYPE(TEMPERATURE_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'waterstatebulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERSTATEBULK_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'waterfluxbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERFLUXBULK_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'energyflux_inst', 'dtype': 'UNKNOWN(TYPE(ENERGYFLUX_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'frictionvel_inst', 'dtype': 'UNKNOWN(TYPE(FRICTIONVEL_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'surfalb_inst', 'dtype': 'UNKNOWN(TYPE(SURFALB_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'solarabs_inst', 'dtype': 'UNKNOWN(TYPE(SOLARABS_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}, {'name': 'wateratm2lndbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERATM2LNDBULK_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'waterdiagnosticbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERDIAGNOSTICBULK_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'getclmvar': {'kind': 'subroutine', 'args': [{'name': 'nstep', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'dtime_clm', 'dtype': 'float64', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'atm2lnd_inst', 'dtype': 'UNKNOWN(TYPE(ATM2LND_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'soilstate_inst', 'dtype': 'UNKNOWN(TYPE(SOILSTATE_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'temperature_inst', 'dtype': 'UNKNOWN(TYPE(TEMPERATURE_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'surfalb_inst', 'dtype': 'UNKNOWN(TYPE(SURFALB_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'wateratm2lndbulk_inst', 'dtype': 'UNKNOWN(TYPE(WATERATM2LNDBULK_TYPE))', 'intent': 'IN', 'optional': False}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}, 'mltimestepfluxintegration': {'kind': 'subroutine', 'args': [{'name': 'nstep_ml', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'num_ml_steps', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'flux_accumulator', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}]}, {'name': 'flux_accumulator_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}]}, {'name': 'flux_accumulator_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}, {'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'IN', 'optional': False}], 'result': None, 'result_dtype': None}, 'canopyfluxesdiagnostics': {'kind': 'subroutine', 'args': [{'name': 'num_filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False}, {'name': 'filter', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': None}]}, {'name': 'mlcanopy_inst', 'dtype': 'UNKNOWN(TYPE(MLCANOPY_TYPE))', 'intent': 'INOUT', 'optional': False}], 'result': None, 'result_dtype': None}}

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

def _make_energyflux_type():
    """factory for type(energyflux_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.eflx_sh_tot_patch = None
    o.eflx_lh_tot_patch = None
    o.eflx_lwrad_out_patch = None
    o.taux_patch = None
    o.tauy_patch = None
    return o

def _make_frictionvel_type():
    """factory for type(frictionvel_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.forc_hgt_u_patch = None
    o.u10_clm_patch = None
    o.fv_patch = None
    return o

def _make_gridcell_type():
    """factory for type(gridcell_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.latdeg = None
    o.londeg = None
    return o

def _make_patch_type():
    """factory for type(patch_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.column = None
    o.gridcell = None
    o.itype = None
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

def _make_solarabs_type():
    """factory for type(solarabs_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.fsa_patch = None
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

def _make_temperature_type():
    """factory for type(temperature_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.t_soisno_col = None
    o.t_a10_patch = None
    o.t_ref2m_patch = None
    return o

def _make_wateratm2lndbulk_type():
    """factory for type(wateratm2lndbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.forc_q_downscaled_col = None
    o.forc_rain_downscaled_col = None
    o.forc_snow_downscaled_col = None
    return o

def _make_waterdiagnosticbulk_type():
    """factory for type(waterdiagnosticbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.q_ref2m_patch = None
    o.frac_sno_eff_col = None
    o.bw_col = None
    return o

def _make_waterfluxbulk_type():
    """factory for type(waterfluxbulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.qflx_evap_tot_patch = None
    return o

def _make_waterstatebulk_type():
    """factory for type(waterstatebulk_type) (components per Derived_Type_Def)."""
    o = _new_derived()
    o.h2osoi_liq_col = None
    o.h2osoi_ice_col = None
    o.h2osoi_vol_col = None
    o.h2osfc_col = None
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


def mlcanopyfluxes(bounds, num_exposedvegp, filter_exposedvegp, atm2lnd_inst, canopystate_inst, soilstate_inst, temperature_inst, waterstatebulk_inst, waterfluxbulk_inst, energyflux_inst, frictionvel_inst, surfalb_inst, solarabs_inst, mlcanopy_inst, wateratm2lndbulk_inst, waterdiagnosticbulk_inst):
    """L51-L695 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    num_mlcan = 0
    filter_mlcan = np.empty((bounds.endp - bounds.begp + 1,), dtype=np.int32)
    fp = 0
    p = 0
    c = 0
    g = 0
    ic = 0
    nstep = 0
    num_ml_steps = 0
    nstep_ml = 0
    dtime_clm = 0.0
    curr_calday_end = 0.0
    curr_calday_beg = 0.0
    calday_interp_bef = 0.0
    calday_interp_cur = 0.0
    calday_interp_next = 0.0
    calday_interp_ml = 0.0
    totpai = 0.0
    flux_accumulator = np.empty(((bounds.endp) - (bounds.begp) + 1, NVAR1D,), dtype=np.float64)
    flux_accumulator_profile = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN + 1, NVAR2D,), dtype=np.float64)
    flux_accumulator_leaf = np.empty(((bounds.endp) - (bounds.begp) + 1, NLEVMLCAN, NLEAF, NVAR3D,), dtype=np.float64)
    irk = 0
    nrk_steps = 0
    ark = np.empty((NRK, NRK,), dtype=np.float64)
    brk = np.empty((NRK,), dtype=np.float64)
    crk = np.empty((NRK,), dtype=np.float64)
    # B001 <- L135-L694
    elai = canopystate_inst.elai_patch
    esai = canopystate_inst.esai_patch
    smp_l = soilstate_inst.smp_l_col
    t_soisno = temperature_inst.t_soisno_col
    eflx_lh_tot = energyflux_inst.eflx_lh_tot_patch
    eflx_sh_tot = energyflux_inst.eflx_sh_tot_patch
    eflx_lwrad_out = energyflux_inst.eflx_lwrad_out_patch
    taux = energyflux_inst.taux_patch
    tauy = energyflux_inst.tauy_patch
    fv = frictionvel_inst.fv_patch
    u10_clm = frictionvel_inst.u10_clm_patch
    fsa = solarabs_inst.fsa_patch
    albd = surfalb_inst.albd_patch
    albi = surfalb_inst.albi_patch
    t_ref2m = temperature_inst.t_ref2m_patch
    qflx_evap_tot = waterfluxbulk_inst.qflx_evap_tot_patch
    q_ref2m = waterdiagnosticbulk_inst.q_ref2m_patch
    zref = mlcanopy_inst.zref_forcing
    tref_bef = mlcanopy_inst.tref_bef_forcing
    tref_cur = mlcanopy_inst.tref_cur_forcing
    qref_bef = mlcanopy_inst.qref_bef_forcing
    qref_cur = mlcanopy_inst.qref_cur_forcing
    uref_bef = mlcanopy_inst.uref_bef_forcing
    uref_cur = mlcanopy_inst.uref_cur_forcing
    pref_bef = mlcanopy_inst.pref_bef_forcing
    pref_cur = mlcanopy_inst.pref_cur_forcing
    co2ref_bef = mlcanopy_inst.co2ref_bef_forcing
    co2ref_cur = mlcanopy_inst.co2ref_cur_forcing
    swskyb_bef = mlcanopy_inst.swskyb_bef_forcing
    swskyb_cur = mlcanopy_inst.swskyb_cur_forcing
    swskyd_bef = mlcanopy_inst.swskyd_bef_forcing
    swskyd_cur = mlcanopy_inst.swskyd_cur_forcing
    lwsky_bef = mlcanopy_inst.lwsky_bef_forcing
    lwsky_cur = mlcanopy_inst.lwsky_cur_forcing
    ncan = mlcanopy_inst.ncan_canopy
    lai = mlcanopy_inst.lai_canopy
    sai = mlcanopy_inst.sai_canopy
    swveg = mlcanopy_inst.swveg_canopy
    lwup = mlcanopy_inst.lwup_canopy
    shflx = mlcanopy_inst.shflx_canopy
    lhflx = mlcanopy_inst.lhflx_canopy
    etflx = mlcanopy_inst.etflx_canopy
    ustar = mlcanopy_inst.ustar_canopy
    swsoi = mlcanopy_inst.swsoi_soil
    lwsoi = mlcanopy_inst.lwsoi_soil
    rnsoi = mlcanopy_inst.rnsoi_soil
    tg = mlcanopy_inst.tg_soil
    tg_bef = mlcanopy_inst.tg_bef_soil
    rhg = mlcanopy_inst.rhg_soil
    dlai = mlcanopy_inst.dlai_profile
    dsai = mlcanopy_inst.dsai_profile
    dpai = mlcanopy_inst.dpai_profile
    dlai_frac = mlcanopy_inst.dlai_frac_profile
    dsai_frac = mlcanopy_inst.dsai_frac_profile
    fracsun = mlcanopy_inst.fracsun_profile
    tair = mlcanopy_inst.tair_profile
    tair_bef = mlcanopy_inst.tair_bef_profile
    eair = mlcanopy_inst.eair_profile
    eair_bef = mlcanopy_inst.eair_bef_profile
    cair = mlcanopy_inst.cair_profile
    cair_bef = mlcanopy_inst.cair_bef_profile
    h2ocan = mlcanopy_inst.h2ocan_profile
    h2ocan_bef = mlcanopy_inst.h2ocan_bef_profile
    swleaf = mlcanopy_inst.swleaf_leaf
    lwleaf = mlcanopy_inst.lwleaf_leaf
    rnleaf = mlcanopy_inst.rnleaf_leaf
    tleaf = mlcanopy_inst.tleaf_leaf
    tleaf_bef = mlcanopy_inst.tleaf_bef_leaf
    tleaf_hist = mlcanopy_inst.tleaf_hist_leaf
    lwp = mlcanopy_inst.lwp_leaf
    lwp_bef = mlcanopy_inst.lwp_bef_leaf
    lwp_hist = mlcanopy_inst.lwp_hist_leaf
    nstep = _clm.get_nstep()
    dtime_clm = _clm.get_step_size()
    curr_calday_end = _clm.get_curr_calday(offset=0)
    curr_calday_beg = _clm.get_curr_calday(offset=(-int(dtime_clm)))
    if (_mlclm.met_type == 0):
        calday_interp_cur = 0.0
        calday_interp_bef = 0.0
        calday_interp_next = 0.0
    elif (_mlclm.met_type == 2):
        raise RuntimeError('endrun')  # endrun (infra stub)
        calday_interp_cur = curr_calday_end
        calday_interp_bef = (calday_interp_cur - (dtime_clm / F_86400P))
        calday_interp_next = 0.0
    elif (_mlclm.met_type == I_3):
        calday_interp_cur = (0.5 * ((curr_calday_end + curr_calday_beg)))
        calday_interp_bef = (calday_interp_cur - (dtime_clm / F_86400P))
        calday_interp_next = (calday_interp_cur + (dtime_clm / F_86400P))
    num_ml_steps = int((dtime_clm / _mlclm.dtime_ml))
    num_mlcan = 0
    for fp in range(1, num_exposedvegp + 1):
        p = filter_exposedvegp[fp - 1]
        g = _patchtype.patch.gridcell[fp - 1]
        num_mlcan = (num_mlcan + 1)
        filter_mlcan[num_mlcan - 1] = p
    _mlclm.ml_vert_init = 0
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        if (zref[p - 1] == SPVAL):
            _mlclm.ml_vert_init = 1
    if (_mlclm.ml_vert_init == 1):
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
        mlcanopy_inst = _mli.getpadparameters(num_mlcan, filter_mlcan, mlcanopy_inst)
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
        mlcanopy_inst = _mli.initverticalstructure(bounds, num_mlcan, filter_mlcan, canopystate_inst, frictionvel_inst, mlcanopy_inst)
        mlcanopy_inst = _mli.initverticalprofiles(num_mlcan, filter_mlcan, atm2lnd_inst, wateratm2lndbulk_inst, mlcanopy_inst)
        if _spmdmod.masterproc:
            pass  # write(iulog,...) log — no dataflow
    _out = _mlr.rungekuttaini(ark, brk, crk)
    _f_copy_out(ark, _out[0])
    _f_copy_out(brk, _out[1])
    _f_copy_out(crk, _out[2])
    mlcanopy_inst = getclmvar(nstep, dtime_clm, num_mlcan, filter_mlcan, atm2lnd_inst, soilstate_inst, temperature_inst, surfalb_inst, wateratm2lndbulk_inst, mlcanopy_inst)
    if (_mlclm.ml_vert_init == 1):
        for fp in range(1, num_mlcan + 1):
            p = filter_mlcan[fp - 1]
            uref_bef[p - 1] = uref_cur[p - 1]
            tref_bef[p - 1] = tref_cur[p - 1]
            qref_bef[p - 1] = qref_cur[p - 1]
            pref_bef[p - 1] = pref_cur[p - 1]
            co2ref_bef[p - 1] = co2ref_cur[p - 1]
            swskyb_bef[p - 1, IVIS - 1] = swskyb_cur[p - 1, IVIS - 1]
            swskyb_bef[p - 1, INIR - 1] = swskyb_cur[p - 1, INIR - 1]
            swskyd_bef[p - 1, IVIS - 1] = swskyd_cur[p - 1, IVIS - 1]
            swskyd_bef[p - 1, INIR - 1] = swskyd_cur[p - 1, INIR - 1]
            lwsky_bef[p - 1] = lwsky_cur[p - 1]
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        lai[p - 1] = elai[p - 1]
        sai[p - 1] = esai[p - 1]
        for ic in range(1, ncan[p - 1] + 1):
            dlai[p - 1, ic - 1] = (dlai_frac[p - 1, ic - 1] * lai[p - 1])
            dsai[p - 1, ic - 1] = (dsai_frac[p - 1, ic - 1] * sai[p - 1])
            dpai[p - 1, ic - 1] = (dlai[p - 1, ic - 1] + dsai[p - 1, ic - 1])
        totpai = np.sum(dpai[p - 1, 0:ncan[p - 1]])
        if (abs((totpai - ((lai[p - 1] + sai[p - 1])))) > F_1PEM06):
            raise RuntimeError('endrun')  # endrun (infra stub)
    mlcanopy_inst = _mlp.soilresistance(num_mlcan, filter_mlcan, soilstate_inst, waterstatebulk_inst, mlcanopy_inst)
    mlcanopy_inst = _mlp.plantresistance(num_mlcan, filter_mlcan, mlcanopy_inst)
    mlcanopy_inst = _mlle.leafheatcapacity(num_mlcan, filter_mlcan, mlcanopy_inst)
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        c = _patchtype.patch.column[p - 1]
        rhg[p - 1] = math.exp(((((_clm_varcon.grav * _mlcl.mmh2o) * smp_l[c - 1, 0]) * F_1PEM03) / ((_mlcl.rgas * t_soisno[c - 1, (1) - (- _clm_varpar.nlevsno + 1)]))))
    for nstep_ml in range(1, num_ml_steps + 1):
        try:  # forward-goto region (label 100)
            if (_mlclm.met_type == 0) or (_mlclm.met_type == 2):
                calday_interp_ml = (curr_calday_beg + (np.float64(nstep_ml) * ((_mlclm.dtime_ml / F_86400P))))
            elif (_mlclm.met_type == I_3):
                calday_interp_ml = (curr_calday_beg + (((np.float64(nstep_ml) - 0.5)) * ((_mlclm.dtime_ml / F_86400P))))
            for fp in range(1, num_mlcan + 1):
                p = filter_mlcan[fp - 1]
                tg_bef[p - 1] = tg[p - 1]
                for ic in range(1, ncan[p - 1] + 1):
                    tair_bef[p - 1, ic - 1] = tair[p - 1, ic - 1]
                    eair_bef[p - 1, ic - 1] = eair[p - 1, ic - 1]
                    cair_bef[p - 1, ic - 1] = cair[p - 1, ic - 1]
                    h2ocan_bef[p - 1, ic - 1] = h2ocan[p - 1, ic - 1]
                    tleaf_bef[p - 1, ic - 1, ISUN - 1] = tleaf[p - 1, ic - 1, ISUN - 1]
                    tleaf_bef[p - 1, ic - 1, ISHA - 1] = tleaf[p - 1, ic - 1, ISHA - 1]
                    lwp_bef[p - 1, ic - 1, ISUN - 1] = lwp[p - 1, ic - 1, ISUN - 1]
                    lwp_bef[p - 1, ic - 1, ISHA - 1] = lwp[p - 1, ic - 1, ISHA - 1]
            mlcanopy_inst = _mlg.getatmforcing(calday_interp_bef, calday_interp_cur, calday_interp_next, calday_interp_ml, num_mlcan, filter_mlcan, mlcanopy_inst)
            mlcanopy_inst = _mls.solarradiation(bounds, num_mlcan, filter_mlcan, mlcanopy_inst)
            mlcanopy_inst = _mlca.canopynitrogenprofile(num_mlcan, filter_mlcan, mlcanopy_inst)
            if (RUNGE_KUTTA_TYPE == I_10):
                nrk_steps = 0
            elif (I_20 <= RUNGE_KUTTA_TYPE):
                nrk_steps = int((RUNGE_KUTTA_TYPE / I_10))
            for irk in range(1, (nrk_steps + 1) + 1):
                mlcanopy_inst = _mlcano.canopywettedfraction(num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mllo.longwaveradiation(bounds, num_mlcan, filter_mlcan, mlcanopy_inst)
                for fp in range(1, num_mlcan + 1):
                    p = filter_mlcan[fp - 1]
                    for ic in range(1, ncan[p - 1] + 1):
                        rnleaf[p - 1, ic - 1, ISUN - 1] = ((swleaf[p - 1, ic - 1, ISUN - 1, IVIS - 1] + swleaf[p - 1, ic - 1, ISUN - 1, INIR - 1]) + lwleaf[p - 1, ic - 1, ISUN - 1])
                        rnleaf[p - 1, ic - 1, ISHA - 1] = ((swleaf[p - 1, ic - 1, ISHA - 1, IVIS - 1] + swleaf[p - 1, ic - 1, ISHA - 1, INIR - 1]) + lwleaf[p - 1, ic - 1, ISHA - 1])
                    rnsoi[p - 1] = ((swsoi[p - 1, IVIS - 1] + swsoi[p - 1, INIR - 1]) + lwsoi[p - 1])
                mlcanopy_inst = _mlcan.canopyturbulence(nstep_ml, num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mll.leafboundarylayer(num_mlcan, filter_mlcan, ISUN, mlcanopy_inst)
                mlcanopy_inst = _mll.leafboundarylayer(num_mlcan, filter_mlcan, ISHA, mlcanopy_inst)
                mlcanopy_inst = _mllea.leafphotosynthesis(num_mlcan, filter_mlcan, ISUN, mlcanopy_inst)
                mlcanopy_inst = _mllea.leafphotosynthesis(num_mlcan, filter_mlcan, ISHA, mlcanopy_inst)
                mlcanopy_inst = _mlf.fluxprofilesolution(num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mlp.leafwaterpotential(num_mlcan, filter_mlcan, ISUN, mlcanopy_inst)
                mlcanopy_inst = _mlp.leafwaterpotential(num_mlcan, filter_mlcan, ISHA, mlcanopy_inst)
                mlcanopy_inst = _mlcano.canopyinterception(num_mlcan, filter_mlcan, mlcanopy_inst)
                mlcanopy_inst = _mlcano.canopyevaporation(num_mlcan, filter_mlcan, mlcanopy_inst)
                if ((nrk_steps > 0) and (irk <= nrk_steps)):
                    mlcanopy_inst = _mlr.rungekuttaupdate(irk, ark, brk, crk, num_mlcan, filter_mlcan, mlcanopy_inst)
            raise _FGoto('100')  # goto 100
            pass  # write(36,...) log — no dataflow
        except _FGoto as _g:
            if _g.args[0] != '100':
                raise
            pass  # 100 (region exit)
        _out = mltimestepfluxintegration(nstep_ml, num_ml_steps, num_mlcan, filter_mlcan, flux_accumulator, flux_accumulator_profile, flux_accumulator_leaf, mlcanopy_inst)
        _f_copy_out(flux_accumulator, _out[0])
        _f_copy_out(flux_accumulator_profile, _out[1])
        _f_copy_out(flux_accumulator_leaf, _out[2])
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        uref_bef[p - 1] = uref_cur[p - 1]
        tref_bef[p - 1] = tref_cur[p - 1]
        qref_bef[p - 1] = qref_cur[p - 1]
        pref_bef[p - 1] = pref_cur[p - 1]
        co2ref_bef[p - 1] = co2ref_cur[p - 1]
        swskyb_bef[p - 1, IVIS - 1] = swskyb_cur[p - 1, IVIS - 1]
        swskyb_bef[p - 1, INIR - 1] = swskyb_cur[p - 1, INIR - 1]
        swskyd_bef[p - 1, IVIS - 1] = swskyd_cur[p - 1, IVIS - 1]
        swskyd_bef[p - 1, INIR - 1] = swskyd_cur[p - 1, INIR - 1]
        lwsky_bef[p - 1] = lwsky_cur[p - 1]
    mlcanopy_inst = canopyfluxesdiagnostics(num_mlcan, filter_mlcan, mlcanopy_inst)
    for fp in range(1, num_mlcan + 1):
        p = filter_mlcan[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            tleaf_hist[p - 1, ic - 1, ISUN - 1] = tleaf[p - 1, ic - 1, ISUN - 1]
            tleaf_hist[p - 1, ic - 1, ISHA - 1] = tleaf[p - 1, ic - 1, ISHA - 1]
            lwp_hist[p - 1, ic - 1, ISUN - 1] = lwp[p - 1, ic - 1, ISUN - 1]
            lwp_hist[p - 1, ic - 1, ISHA - 1] = lwp[p - 1, ic - 1, ISHA - 1]
            if (dpai[p - 1, ic - 1] > 0.0):
                tleaf[p - 1, ic - 1, ISUN - 1] = ((tleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (tleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                tleaf[p - 1, ic - 1, ISHA - 1] = tleaf[p - 1, ic - 1, ISUN - 1]
                lwp[p - 1, ic - 1, ISUN - 1] = ((lwp[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lwp[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lwp[p - 1, ic - 1, ISHA - 1] = lwp[p - 1, ic - 1, ISUN - 1]
    if (_mlclm.mlcan_to_clm == 1):
        for fp in range(1, num_mlcan + 1):
            p = filter_mlcan[fp - 1]
            albd[p - 1, IVIS - 1] = 0.0
            albd[p - 1, INIR - 1] = 0.0
            albi[p - 1, IVIS - 1] = 0.0
            albi[p - 1, INIR - 1] = 0.0
            taux[p - 1] = 0.0
            tauy[p - 1] = 0.0
            eflx_lh_tot[p - 1] = lhflx[p - 1]
            eflx_sh_tot[p - 1] = shflx[p - 1]
            eflx_lwrad_out[p - 1] = lwup[p - 1]
            qflx_evap_tot[p - 1] = (etflx[p - 1] * _mlcl.mmh2o)
            fv[p - 1] = ustar[p - 1]
            u10_clm[p - 1] = 0.0
            t_ref2m[p - 1] = 0.0
            q_ref2m[p - 1] = 0.0
            fsa[p - 1] = (((swveg[p - 1, IVIS - 1] + swveg[p - 1, INIR - 1]) + swsoi[p - 1, IVIS - 1]) + swsoi[p - 1, INIR - 1])
    return canopystate_inst, soilstate_inst, temperature_inst, waterstatebulk_inst, waterfluxbulk_inst, energyflux_inst, frictionvel_inst, surfalb_inst, solarabs_inst, mlcanopy_inst, waterdiagnosticbulk_inst

def getclmvar(nstep, dtime_clm, num_filter, filter, atm2lnd_inst, soilstate_inst, temperature_inst, surfalb_inst, wateratm2lndbulk_inst, mlcanopy_inst):
    """L698-L868 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    c = 0
    g = 0
    lat = 0.0
    lon = 0.0
    coszen = 0.0
    caldaym1 = 0.0
    declinm1 = 0.0
    eccf = 0.0
    # B001 <- L738-L867
    forc_u = atm2lnd_inst.forc_u_grc
    forc_v = atm2lnd_inst.forc_v_grc
    forc_pco2 = atm2lnd_inst.forc_pco2_grc
    forc_po2 = atm2lnd_inst.forc_po2_grc
    forc_solad_col = atm2lnd_inst.forc_solad_downscaled_col
    forc_solai = atm2lnd_inst.forc_solai_grc
    forc_t = atm2lnd_inst.forc_t_downscaled_col
    forc_pbot = atm2lnd_inst.forc_pbot_downscaled_col
    forc_lwrad = atm2lnd_inst.forc_lwrad_downscaled_col
    forc_q = wateratm2lndbulk_inst.forc_q_downscaled_col
    forc_rain = wateratm2lndbulk_inst.forc_rain_downscaled_col
    forc_snow = wateratm2lndbulk_inst.forc_snow_downscaled_col
    albgrd = surfalb_inst.albgrd_col
    albgri = surfalb_inst.albgri_col
    soilresis = soilstate_inst.soilresis_col
    thk = soilstate_inst.thk_col
    t_a10_patch = temperature_inst.t_a10_patch
    t_soisno = temperature_inst.t_soisno_col
    snl = _columntype.col.snl
    z = _columntype.col.z
    zi = _columntype.col.zi
    tref_cur = mlcanopy_inst.tref_cur_forcing
    qref_cur = mlcanopy_inst.qref_cur_forcing
    uref_cur = mlcanopy_inst.uref_cur_forcing
    pref_cur = mlcanopy_inst.pref_cur_forcing
    co2ref_cur = mlcanopy_inst.co2ref_cur_forcing
    o2ref = mlcanopy_inst.o2ref_forcing
    solar_zen = mlcanopy_inst.solar_zen_forcing
    swskyb_cur = mlcanopy_inst.swskyb_cur_forcing
    swskyd_cur = mlcanopy_inst.swskyd_cur_forcing
    lwsky_cur = mlcanopy_inst.lwsky_cur_forcing
    qflx_rain = mlcanopy_inst.qflx_rain_forcing
    qflx_snow = mlcanopy_inst.qflx_snow_forcing
    tacclim = mlcanopy_inst.tacclim_forcing
    albsoib = mlcanopy_inst.albsoib_soil
    albsoid = mlcanopy_inst.albsoid_soil
    soilres = mlcanopy_inst.soilres_soil
    soil_t = mlcanopy_inst.soil_t_soil
    soil_dz = mlcanopy_inst.soil_dz_soil
    soil_tk = mlcanopy_inst.soil_tk_soil
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        c = _patchtype.patch.column[p - 1]
        g = _patchtype.patch.gridcell[p - 1]
        uref_cur[p - 1] = math.sqrt(((forc_u[g - 1] * forc_u[g - 1]) + (forc_v[g - 1] * forc_v[g - 1])))
        swskyd_cur[p - 1, IVIS - 1] = forc_solai[g - 1, IVIS - 1]
        swskyd_cur[p - 1, INIR - 1] = forc_solai[g - 1, INIR - 1]
        tref_cur[p - 1] = forc_t[c - 1]
        qref_cur[p - 1] = forc_q[c - 1]
        pref_cur[p - 1] = forc_pbot[c - 1]
        lwsky_cur[p - 1] = forc_lwrad[c - 1]
        qflx_rain[p - 1] = forc_rain[c - 1]
        qflx_snow[p - 1] = forc_snow[c - 1]
        swskyb_cur[p - 1, IVIS - 1] = forc_solad_col[c - 1, IVIS - 1]
        swskyb_cur[p - 1, INIR - 1] = forc_solad_col[c - 1, INIR - 1]
        co2ref_cur[p - 1] = ((forc_pco2[g - 1] / forc_pbot[c - 1]) * F_1PE06)
        o2ref[p - 1] = ((forc_po2[g - 1] / forc_pbot[c - 1]) * F_1PE03)
        tacclim[p - 1] = t_a10_patch[p - 1]
        albsoib[p - 1, IVIS - 1] = albgrd[c - 1, IVIS - 1]
        albsoib[p - 1, INIR - 1] = albgrd[c - 1, INIR - 1]
        albsoid[p - 1, IVIS - 1] = albgri[c - 1, IVIS - 1]
        albsoid[p - 1, INIR - 1] = albgri[c - 1, INIR - 1]
        soilres[p - 1] = soilresis[c - 1]
        soil_t[p - 1] = t_soisno[c - 1, ((snl[c - 1] + 1)) - (- _clm_varpar.nlevsno + 1)]
        soil_dz[p - 1] = ((z[c - 1, ((snl[c - 1] + 1)) - (- _clm_varpar.nlevsno + 1)] - zi[c - 1, (snl[c - 1]) - (- _clm_varpar.nlevsno + 0)]))
        soil_tk[p - 1] = thk[c - 1, ((snl[c - 1] + 1)) - (- _clm_varpar.nlevsno + 1)]
    caldaym1 = _clm.get_curr_calday(offset=(-int(dtime_clm)))
    declinm1, eccf = _shr.shr_orb_decl(caldaym1, _clm_varorb.eccen, _clm_varorb.mvelpp, _clm_varorb.lambm0, _clm_varorb.obliqr)
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        c = _patchtype.patch.column[p - 1]
        g = _patchtype.patch.gridcell[p - 1]
        lat = ((_gri.grc.latdeg[g - 1] * _clm_varcon.rpi) / F_180P)
        lon = ((_gri.grc.londeg[g - 1] * _clm_varcon.rpi) / F_180P)
        coszen = _shr.shr_orb_cosz(caldaym1, lat, lon, declinm1)
        solar_zen[p - 1] = math.acos(_f_max(F_0P01, coszen))
    return mlcanopy_inst

def mltimestepfluxintegration(nstep_ml, num_ml_steps, num_filter, filter, flux_accumulator, flux_accumulator_profile, flux_accumulator_leaf, mlcanopy_inst):
    """L871-L1096 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    i = 0
    j = 0
    k = 0
    # B001 <- L897-L1095
    swskyb = mlcanopy_inst.swskyb_forcing
    swskyd = mlcanopy_inst.swskyd_forcing
    lwsky = mlcanopy_inst.lwsky_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ustar = mlcanopy_inst.ustar_canopy
    beta = mlcanopy_inst.beta_canopy
    obu = mlcanopy_inst.obu_canopy
    z0m = mlcanopy_inst.z0m_canopy
    zdisp = mlcanopy_inst.zdisp_canopy
    lwup = mlcanopy_inst.lwup_canopy
    qflx_intr = mlcanopy_inst.qflx_intr_canopy
    qflx_tflrain = mlcanopy_inst.qflx_tflrain_canopy
    qflx_tflsnow = mlcanopy_inst.qflx_tflsnow_canopy
    swsoi = mlcanopy_inst.swsoi_soil
    lwsoi = mlcanopy_inst.lwsoi_soil
    rnsoi = mlcanopy_inst.rnsoi_soil
    shsoi = mlcanopy_inst.shsoi_soil
    lhsoi = mlcanopy_inst.lhsoi_soil
    etsoi = mlcanopy_inst.etsoi_soil
    gsoi = mlcanopy_inst.gsoi_soil
    gac0 = mlcanopy_inst.gac0_soil
    shair = mlcanopy_inst.shair_profile
    etair = mlcanopy_inst.etair_profile
    stair = mlcanopy_inst.stair_profile
    mflx = mlcanopy_inst.mflx_profile
    kc_eddy = mlcanopy_inst.kc_eddy_profile
    gac = mlcanopy_inst.gac_profile
    swupw = mlcanopy_inst.swupw_profile
    swdwn = mlcanopy_inst.swdwn_profile
    swbeam = mlcanopy_inst.swbeam_profile
    lwupw = mlcanopy_inst.lwupw_profile
    lwdwn = mlcanopy_inst.lwdwn_profile
    swleaf = mlcanopy_inst.swleaf_leaf
    lwleaf = mlcanopy_inst.lwleaf_leaf
    rnleaf = mlcanopy_inst.rnleaf_leaf
    shleaf = mlcanopy_inst.shleaf_leaf
    lhleaf = mlcanopy_inst.lhleaf_leaf
    trleaf = mlcanopy_inst.trleaf_leaf
    evleaf = mlcanopy_inst.evleaf_leaf
    stleaf = mlcanopy_inst.stleaf_leaf
    anet = mlcanopy_inst.anet_leaf
    agross = mlcanopy_inst.agross_leaf
    gs = mlcanopy_inst.gs_leaf
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        if (nstep_ml == 1):
            flux_accumulator[p - 1, :] = 0.0
            flux_accumulator_profile[p - 1, :, :] = 0.0
            flux_accumulator_leaf[p - 1, :, :, :] = 0.0
        i = 0
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + ustar[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + beta[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + obu[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + z0m[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + zdisp[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lwup[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swsoi[p - 1, IVIS - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swsoi[p - 1, INIR - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lwsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + rnsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + shsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lhsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + etsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + gsoi[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + gac0[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + qflx_intr[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + qflx_tflrain[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + qflx_tflsnow[p - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyb[p - 1, IVIS - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyb[p - 1, INIR - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyd[p - 1, IVIS - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + swskyd[p - 1, INIR - 1])
        i = (i + 1)
        flux_accumulator[p - 1, i - 1] = (flux_accumulator[p - 1, i - 1] + lwsky[p - 1])
        j = 0
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + shair[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + etair[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + stair[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + mflx[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + kc_eddy[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] = (flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1] + gac[p - 1, 0:ncan[p - 1]])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swupw[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, IVIS - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swupw[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, INIR - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swdwn[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, IVIS - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swdwn[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, INIR - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swbeam[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, IVIS - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + swbeam[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, INIR - 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + lwupw[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1])
        j = (j + 1)
        flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] = (flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1] + lwdwn[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1])
        k = 0
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + swleaf[p - 1, :, :, IVIS - 1])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + swleaf[p - 1, :, :, INIR - 1])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + lwleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + rnleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + shleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + lhleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + trleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + evleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + stleaf[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + anet[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + agross[p - 1, :, :])
        k = (k + 1)
        flux_accumulator_leaf[p - 1, :, :, k - 1] = (flux_accumulator_leaf[p - 1, :, :, k - 1] + gs[p - 1, :, :])
        if (((i > NVAR1D) or (j > NVAR2D)) or (k > NVAR3D)):
            raise RuntimeError('endrun')  # endrun (infra stub)
        if (nstep_ml == num_ml_steps):
            flux_accumulator[p - 1, :] = (flux_accumulator[p - 1, :] / np.float64(num_ml_steps))
            flux_accumulator_profile[p - 1, :, :] = (flux_accumulator_profile[p - 1, :, :] / np.float64(num_ml_steps))
            flux_accumulator_leaf[p - 1, :, :, :] = (flux_accumulator_leaf[p - 1, :, :, :] / np.float64(num_ml_steps))
            i = 0
            i = (i + 1)
            ustar[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            beta[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            obu[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            z0m[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            zdisp[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lwup[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swsoi[p - 1, IVIS - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swsoi[p - 1, INIR - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lwsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            rnsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            shsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lhsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            etsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            gsoi[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            gac0[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            qflx_intr[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            qflx_tflrain[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            qflx_tflsnow[p - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyb[p - 1, IVIS - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyb[p - 1, INIR - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyd[p - 1, IVIS - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            swskyd[p - 1, INIR - 1] = flux_accumulator[p - 1, i - 1]
            i = (i + 1)
            lwsky[p - 1] = flux_accumulator[p - 1, i - 1]
            j = 0
            j = (j + 1)
            shair[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            etair[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            stair[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            mflx[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            kc_eddy[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            gac[p - 1, 0:ncan[p - 1]] = flux_accumulator_profile[p - 1, 0:ncan[p - 1], j - 1]
            j = (j + 1)
            swupw[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, IVIS - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swupw[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, INIR - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swdwn[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, IVIS - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swdwn[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, INIR - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swbeam[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, IVIS - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            swbeam[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1, INIR - 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            lwupw[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            j = (j + 1)
            lwdwn[p - 1, (0) - (0):(ncan[p - 1]) - (0) + 1] = flux_accumulator_profile[p - 1, 0:(ncan[p - 1] + 1), j - 1]
            k = 0
            k = (k + 1)
            swleaf[p - 1, :, :, IVIS - 1] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            swleaf[p - 1, :, :, INIR - 1] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            lwleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            rnleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            shleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            lhleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            trleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            evleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            stleaf[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            anet[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            agross[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            k = (k + 1)
            gs[p - 1, :, :] = flux_accumulator_leaf[p - 1, :, :, k - 1]
            if (((i > NVAR1D) or (j > NVAR2D)) or (k > NVAR3D)):
                raise RuntimeError('endrun')  # endrun (infra stub)
    return flux_accumulator, flux_accumulator_profile, flux_accumulator_leaf

def canopyfluxesdiagnostics(num_filter, filter, mlcanopy_inst):
    """L1099-L1512 subroutine (machine-translated)."""
    # UB-guard + automatic-array allocation (Fortran locals undefined until assignment)
    fp = 0
    p = 0
    ic = 0
    ib = 0
    err = 0.0
    radin = 0.0
    radout = 0.0
    avail = 0.0
    flux = 0.0
    fracgreen = 0.0
    minlwp = 0.0
    # B001 <- L1131-L1511
    tref = mlcanopy_inst.tref_forcing
    swskyb = mlcanopy_inst.swskyb_forcing
    swskyd = mlcanopy_inst.swskyd_forcing
    lwsky = mlcanopy_inst.lwsky_forcing
    ncan = mlcanopy_inst.ncan_canopy
    ntop = mlcanopy_inst.ntop_canopy
    lai = mlcanopy_inst.lai_canopy
    sai = mlcanopy_inst.sai_canopy
    lwup = mlcanopy_inst.lwup_canopy
    shsoi = mlcanopy_inst.shsoi_soil
    lhsoi = mlcanopy_inst.lhsoi_soil
    gsoi = mlcanopy_inst.gsoi_soil
    swsoi = mlcanopy_inst.swsoi_soil
    lwsoi = mlcanopy_inst.lwsoi_soil
    etsoi = mlcanopy_inst.etsoi_soil
    dpai = mlcanopy_inst.dpai_profile
    fwet = mlcanopy_inst.fwet_profile
    fdry = mlcanopy_inst.fdry_profile
    tair = mlcanopy_inst.tair_profile
    wind = mlcanopy_inst.wind_profile
    shair = mlcanopy_inst.shair_profile
    etair = mlcanopy_inst.etair_profile
    stair = mlcanopy_inst.stair_profile
    lwupw = mlcanopy_inst.lwupw_profile
    lwdwn = mlcanopy_inst.lwdwn_profile
    swupw = mlcanopy_inst.swupw_profile
    swdwn = mlcanopy_inst.swdwn_profile
    swbeam = mlcanopy_inst.swbeam_profile
    fracsun = mlcanopy_inst.fracsun_profile
    vcmax25_profile = mlcanopy_inst.vcmax25_profile
    lwleaf = mlcanopy_inst.lwleaf_leaf
    rnleaf = mlcanopy_inst.rnleaf_leaf
    stleaf = mlcanopy_inst.stleaf_leaf
    shleaf = mlcanopy_inst.shleaf_leaf
    lhleaf = mlcanopy_inst.lhleaf_leaf
    trleaf = mlcanopy_inst.trleaf_leaf
    evleaf = mlcanopy_inst.evleaf_leaf
    swleaf = mlcanopy_inst.swleaf_leaf
    agross = mlcanopy_inst.agross_leaf
    apar = mlcanopy_inst.apar_leaf
    anet = mlcanopy_inst.anet_leaf
    gs = mlcanopy_inst.gs_leaf
    tleaf = mlcanopy_inst.tleaf_leaf
    lwp = mlcanopy_inst.lwp_leaf
    vcmax25_leaf = mlcanopy_inst.vcmax25_leaf
    rnet = mlcanopy_inst.rnet_canopy
    stflx_air = mlcanopy_inst.stflx_air_canopy
    stflx_veg = mlcanopy_inst.stflx_veg_canopy
    shflx = mlcanopy_inst.shflx_canopy
    lhflx = mlcanopy_inst.lhflx_canopy
    etflx = mlcanopy_inst.etflx_canopy
    albcan = mlcanopy_inst.albcan_canopy
    swveg = mlcanopy_inst.swveg_canopy
    swvegsun = mlcanopy_inst.swvegsun_canopy
    swvegsha = mlcanopy_inst.swvegsha_canopy
    lwveg = mlcanopy_inst.lwveg_canopy
    lwvegsun = mlcanopy_inst.lwvegsun_canopy
    lwvegsha = mlcanopy_inst.lwvegsha_canopy
    shveg = mlcanopy_inst.shveg_canopy
    shvegsun = mlcanopy_inst.shvegsun_canopy
    shvegsha = mlcanopy_inst.shvegsha_canopy
    lhveg = mlcanopy_inst.lhveg_canopy
    lhvegsun = mlcanopy_inst.lhvegsun_canopy
    lhvegsha = mlcanopy_inst.lhvegsha_canopy
    etveg = mlcanopy_inst.etveg_canopy
    etvegsun = mlcanopy_inst.etvegsun_canopy
    etvegsha = mlcanopy_inst.etvegsha_canopy
    trveg = mlcanopy_inst.trveg_canopy
    evveg = mlcanopy_inst.evveg_canopy
    gppveg = mlcanopy_inst.gppveg_canopy
    gppvegsun = mlcanopy_inst.gppvegsun_canopy
    gppvegsha = mlcanopy_inst.gppvegsha_canopy
    vcmax25veg = mlcanopy_inst.vcmax25veg_canopy
    vcmax25sun = mlcanopy_inst.vcmax25sun_canopy
    vcmax25sha = mlcanopy_inst.vcmax25sha_canopy
    gsveg = mlcanopy_inst.gsveg_canopy
    gsvegsun = mlcanopy_inst.gsvegsun_canopy
    gsvegsha = mlcanopy_inst.gsvegsha_canopy
    windveg = mlcanopy_inst.windveg_canopy
    windvegsun = mlcanopy_inst.windvegsun_canopy
    windvegsha = mlcanopy_inst.windvegsha_canopy
    tlveg = mlcanopy_inst.tlveg_canopy
    tlvegsun = mlcanopy_inst.tlvegsun_canopy
    tlvegsha = mlcanopy_inst.tlvegsha_canopy
    taveg = mlcanopy_inst.taveg_canopy
    tavegsun = mlcanopy_inst.tavegsun_canopy
    tavegsha = mlcanopy_inst.tavegsha_canopy
    laisun = mlcanopy_inst.laisun_canopy
    laisha = mlcanopy_inst.laisha_canopy
    fracminlwp = mlcanopy_inst.fracminlwp_canopy
    swsrc = mlcanopy_inst.swsrc_profile
    lwsrc = mlcanopy_inst.lwsrc_profile
    rnsrc = mlcanopy_inst.rnsrc_profile
    stsrc = mlcanopy_inst.stsrc_profile
    shsrc = mlcanopy_inst.shsrc_profile
    lhsrc = mlcanopy_inst.lhsrc_profile
    etsrc = mlcanopy_inst.etsrc_profile
    trsrc = mlcanopy_inst.trsrc_profile
    evsrc = mlcanopy_inst.evsrc_profile
    fco2src = mlcanopy_inst.fco2src_profile
    swleaf_mean = mlcanopy_inst.swleaf_mean_profile
    lwleaf_mean = mlcanopy_inst.lwleaf_mean_profile
    rnleaf_mean = mlcanopy_inst.rnleaf_mean_profile
    stleaf_mean = mlcanopy_inst.stleaf_mean_profile
    shleaf_mean = mlcanopy_inst.shleaf_mean_profile
    lhleaf_mean = mlcanopy_inst.lhleaf_mean_profile
    etleaf_mean = mlcanopy_inst.etleaf_mean_profile
    trleaf_mean = mlcanopy_inst.trleaf_mean_profile
    evleaf_mean = mlcanopy_inst.evleaf_mean_profile
    fco2_mean = mlcanopy_inst.fco2_mean_profile
    apar_mean = mlcanopy_inst.apar_mean_profile
    gs_mean = mlcanopy_inst.gs_mean_profile
    tleaf_mean = mlcanopy_inst.tleaf_mean_profile
    lwp_mean = mlcanopy_inst.lwp_mean_profile
    for fp in range(1, num_filter + 1):
        p = filter[fp - 1]
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                lwleaf_mean[p - 1, ic - 1] = ((lwleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lwleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                swleaf_mean[p - 1, ic - 1, IVIS - 1] = ((swleaf[p - 1, ic - 1, ISUN - 1, IVIS - 1] * fracsun[p - 1, ic - 1]) + (swleaf[p - 1, ic - 1, ISHA - 1, IVIS - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                swleaf_mean[p - 1, ic - 1, INIR - 1] = ((swleaf[p - 1, ic - 1, ISUN - 1, INIR - 1] * fracsun[p - 1, ic - 1]) + (swleaf[p - 1, ic - 1, ISHA - 1, INIR - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                rnleaf_mean[p - 1, ic - 1] = ((rnleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (rnleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                stleaf_mean[p - 1, ic - 1] = ((stleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (stleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                shleaf_mean[p - 1, ic - 1] = ((shleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (shleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lhleaf_mean[p - 1, ic - 1] = ((lhleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lhleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                etleaf_mean[p - 1, ic - 1] = ((((evleaf[p - 1, ic - 1, ISUN - 1] + trleaf[p - 1, ic - 1, ISUN - 1])) * fracsun[p - 1, ic - 1]) + (((evleaf[p - 1, ic - 1, ISHA - 1] + trleaf[p - 1, ic - 1, ISHA - 1])) * ((1.0 - fracsun[p - 1, ic - 1]))))
                trleaf_mean[p - 1, ic - 1] = ((trleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (trleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                evleaf_mean[p - 1, ic - 1] = ((evleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (evleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                fco2_mean[p - 1, ic - 1] = ((anet[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (anet[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                apar_mean[p - 1, ic - 1] = ((apar[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (apar[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                gs_mean[p - 1, ic - 1] = ((gs[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (gs[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                tleaf_mean[p - 1, ic - 1] = ((tleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (tleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lwp_mean[p - 1, ic - 1] = ((lwp[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (lwp[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))
                lwsrc[p - 1, ic - 1] = (lwleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                swsrc[p - 1, ic - 1, IVIS - 1] = (swleaf_mean[p - 1, ic - 1, IVIS - 1] * dpai[p - 1, ic - 1])
                swsrc[p - 1, ic - 1, INIR - 1] = (swleaf_mean[p - 1, ic - 1, INIR - 1] * dpai[p - 1, ic - 1])
                rnsrc[p - 1, ic - 1] = (rnleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                stsrc[p - 1, ic - 1] = (stleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                shsrc[p - 1, ic - 1] = (shleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                lhsrc[p - 1, ic - 1] = (lhleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                etsrc[p - 1, ic - 1] = (etleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                trsrc[p - 1, ic - 1] = (trleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                evsrc[p - 1, ic - 1] = (evleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1])
                fracgreen = (fdry[p - 1, ic - 1] / ((1.0 - fwet[p - 1, ic - 1])))
                fco2src[p - 1, ic - 1] = (((((anet[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (anet[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))) * dpai[p - 1, ic - 1]) * fracgreen)
            else:
                lwleaf_mean[p - 1, ic - 1] = 0.0
                swleaf_mean[p - 1, ic - 1, IVIS - 1] = 0.0
                swleaf_mean[p - 1, ic - 1, INIR - 1] = 0.0
                rnleaf_mean[p - 1, ic - 1] = 0.0
                stleaf_mean[p - 1, ic - 1] = 0.0
                shleaf_mean[p - 1, ic - 1] = 0.0
                lhleaf_mean[p - 1, ic - 1] = 0.0
                etleaf_mean[p - 1, ic - 1] = 0.0
                trleaf_mean[p - 1, ic - 1] = 0.0
                evleaf_mean[p - 1, ic - 1] = 0.0
                fco2_mean[p - 1, ic - 1] = 0.0
                apar_mean[p - 1, ic - 1] = 0.0
                gs_mean[p - 1, ic - 1] = 0.0
                tleaf_mean[p - 1, ic - 1] = 0.0
                lwp_mean[p - 1, ic - 1] = 0.0
                lwsrc[p - 1, ic - 1] = 0.0
                swsrc[p - 1, ic - 1, IVIS - 1] = 0.0
                swsrc[p - 1, ic - 1, INIR - 1] = 0.0
                rnsrc[p - 1, ic - 1] = 0.0
                stsrc[p - 1, ic - 1] = 0.0
                shsrc[p - 1, ic - 1] = 0.0
                lhsrc[p - 1, ic - 1] = 0.0
                etsrc[p - 1, ic - 1] = 0.0
                trsrc[p - 1, ic - 1] = 0.0
                evsrc[p - 1, ic - 1] = 0.0
                fco2src[p - 1, ic - 1] = 0.0
        swveg[p - 1, IVIS - 1] = 0.0
        swveg[p - 1, INIR - 1] = 0.0
        lwveg[p - 1] = 0.0
        stflx_veg[p - 1] = 0.0
        shveg[p - 1] = 0.0
        lhveg[p - 1] = 0.0
        etveg[p - 1] = 0.0
        trveg[p - 1] = 0.0
        evveg[p - 1] = 0.0
        gppveg[p - 1] = 0.0
        vcmax25veg[p - 1] = 0.0
        gsveg[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            swveg[p - 1, IVIS - 1] = (swveg[p - 1, IVIS - 1] + swsrc[p - 1, ic - 1, IVIS - 1])
            swveg[p - 1, INIR - 1] = (swveg[p - 1, INIR - 1] + swsrc[p - 1, ic - 1, INIR - 1])
            lwveg[p - 1] = (lwveg[p - 1] + lwsrc[p - 1, ic - 1])
            stflx_veg[p - 1] = (stflx_veg[p - 1] + stsrc[p - 1, ic - 1])
            shveg[p - 1] = (shveg[p - 1] + shsrc[p - 1, ic - 1])
            lhveg[p - 1] = (lhveg[p - 1] + lhsrc[p - 1, ic - 1])
            etveg[p - 1] = (etveg[p - 1] + etsrc[p - 1, ic - 1])
            trveg[p - 1] = (trveg[p - 1] + trsrc[p - 1, ic - 1])
            evveg[p - 1] = (evveg[p - 1] + evsrc[p - 1, ic - 1])
            if (dpai[p - 1, ic - 1] > 0.0):
                fracgreen = (fdry[p - 1, ic - 1] / ((1.0 - fwet[p - 1, ic - 1])))
                gppveg[p - 1] = (gppveg[p - 1] + (((((agross[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) + (agross[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))))) * dpai[p - 1, ic - 1]) * fracgreen))
                gsveg[p - 1] = (gsveg[p - 1] + (gs_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1]))
            vcmax25veg[p - 1] = (vcmax25veg[p - 1] + (vcmax25_profile[p - 1, ic - 1] * dpai[p - 1, ic - 1]))
        err = (((((swveg[p - 1, IVIS - 1] + swveg[p - 1, INIR - 1]) + lwveg[p - 1]) - shveg[p - 1]) - lhveg[p - 1]) - stflx_veg[p - 1])
        if (abs(err) >= F_1PEM03):
            raise RuntimeError('endrun')  # endrun (infra stub)
        for ib in range(1, NUMRAD + 1):
            radin = (swskyb[p - 1, ib - 1] + swskyd[p - 1, ib - 1])
            if (radin > 0.0):
                albcan[p - 1, ib - 1] = (swupw[p - 1, (ntop[p - 1]) - (0), ib - 1] / radin)
            else:
                albcan[p - 1, ib - 1] = 0.0
        if (_mlclm.flux_profile_type == 0) or (_mlclm.flux_profile_type == (-1)):
            shflx[p - 1] = (shveg[p - 1] + shsoi[p - 1])
            etflx[p - 1] = (etveg[p - 1] + etsoi[p - 1])
            lhflx[p - 1] = (lhveg[p - 1] + lhsoi[p - 1])
        elif (_mlclm.flux_profile_type == 1):
            shflx[p - 1] = shair[p - 1, ncan[p - 1] - 1]
            etflx[p - 1] = etair[p - 1, ncan[p - 1] - 1]
            lhflx[p - 1] = (etair[p - 1, ncan[p - 1] - 1] * _mlw.latvap(tref[p - 1]))
        else:
            raise RuntimeError('endrun')  # endrun (infra stub)
        stflx_air[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            stflx_air[p - 1] = (stflx_air[p - 1] + stair[p - 1, ic - 1])
        rnet[p - 1] = (((((swveg[p - 1, IVIS - 1] + swveg[p - 1, INIR - 1]) + swsoi[p - 1, IVIS - 1]) + swsoi[p - 1, INIR - 1]) + lwveg[p - 1]) + lwsoi[p - 1])
        radin = ((((swskyb[p - 1, IVIS - 1] + swskyd[p - 1, IVIS - 1]) + swskyb[p - 1, INIR - 1]) + swskyd[p - 1, INIR - 1]) + lwsky[p - 1])
        radout = (((albcan[p - 1, IVIS - 1] * ((swskyb[p - 1, IVIS - 1] + swskyd[p - 1, IVIS - 1]))) + (albcan[p - 1, INIR - 1] * ((swskyb[p - 1, INIR - 1] + swskyd[p - 1, INIR - 1])))) + lwup[p - 1])
        err = (rnet[p - 1] - ((radin - radout)))
        if (abs(err) > F_0P001):
            raise RuntimeError('endrun')  # endrun (infra stub)
        avail = ((radin - radout) - gsoi[p - 1])
        flux = (((shflx[p - 1] + lhflx[p - 1]) + stflx_air[p - 1]) + stflx_veg[p - 1])
        err = (avail - flux)
        if (abs(err) > F_0P01):
            raise RuntimeError('endrun')  # endrun (infra stub)
        ic = int(ntop[p - 1])
        radin = ((((swbeam[p - 1, (ic) - (0), IVIS - 1] + swbeam[p - 1, (ic) - (0), INIR - 1]) + swdwn[p - 1, (ic) - (0), IVIS - 1]) + swdwn[p - 1, (ic) - (0), INIR - 1]) + lwdwn[p - 1, (ic) - (0)])
        radout = ((swupw[p - 1, (ic) - (0), IVIS - 1] + swupw[p - 1, (ic) - (0), INIR - 1]) + lwupw[p - 1, (ic) - (0)])
        err = (((radin - radout)) - rnet[p - 1])
        if (abs(err) > F_0P001):
            raise RuntimeError('endrun')  # endrun (infra stub)
        laisun[p - 1] = 0.0
        laisha[p - 1] = 0.0
        swvegsun[p - 1, 0:NUMRAD] = 0.0
        swvegsha[p - 1, 0:NUMRAD] = 0.0
        lwvegsun[p - 1] = 0.0
        lwvegsha[p - 1] = 0.0
        shvegsun[p - 1] = 0.0
        shvegsha[p - 1] = 0.0
        lhvegsun[p - 1] = 0.0
        lhvegsha[p - 1] = 0.0
        etvegsun[p - 1] = 0.0
        etvegsha[p - 1] = 0.0
        gppvegsun[p - 1] = 0.0
        gppvegsha[p - 1] = 0.0
        vcmax25sun[p - 1] = 0.0
        vcmax25sha[p - 1] = 0.0
        gsvegsun[p - 1] = 0.0
        gsvegsha[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                laisun[p - 1] = (laisun[p - 1] + (fracsun[p - 1, ic - 1] * dpai[p - 1, ic - 1]))
                laisha[p - 1] = (laisha[p - 1] + (((1.0 - fracsun[p - 1, ic - 1])) * dpai[p - 1, ic - 1]))
                swvegsun[p - 1, IVIS - 1] = (swvegsun[p - 1, IVIS - 1] + ((swleaf[p - 1, ic - 1, ISUN - 1, IVIS - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                swvegsun[p - 1, INIR - 1] = (swvegsun[p - 1, INIR - 1] + ((swleaf[p - 1, ic - 1, ISUN - 1, INIR - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                swvegsha[p - 1, IVIS - 1] = (swvegsha[p - 1, IVIS - 1] + ((swleaf[p - 1, ic - 1, ISHA - 1, IVIS - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                swvegsha[p - 1, INIR - 1] = (swvegsha[p - 1, INIR - 1] + ((swleaf[p - 1, ic - 1, ISHA - 1, INIR - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                lwvegsun[p - 1] = (lwvegsun[p - 1] + ((lwleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                lwvegsha[p - 1] = (lwvegsha[p - 1] + ((lwleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                shvegsun[p - 1] = (shvegsun[p - 1] + ((shleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                shvegsha[p - 1] = (shvegsha[p - 1] + ((shleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                lhvegsun[p - 1] = (lhvegsun[p - 1] + ((lhleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                lhvegsha[p - 1] = (lhvegsha[p - 1] + ((lhleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                etvegsun[p - 1] = (etvegsun[p - 1] + ((((evleaf[p - 1, ic - 1, ISUN - 1] + trleaf[p - 1, ic - 1, ISUN - 1])) * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                etvegsha[p - 1] = (etvegsha[p - 1] + ((((evleaf[p - 1, ic - 1, ISHA - 1] + trleaf[p - 1, ic - 1, ISHA - 1])) * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                fracgreen = (fdry[p - 1, ic - 1] / ((1.0 - fwet[p - 1, ic - 1])))
                gppvegsun[p - 1] = (gppvegsun[p - 1] + (((agross[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) * fracgreen))
                gppvegsha[p - 1] = (gppvegsha[p - 1] + (((agross[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) * fracgreen))
                vcmax25sun[p - 1] = (vcmax25sun[p - 1] + ((vcmax25_leaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                vcmax25sha[p - 1] = (vcmax25sha[p - 1] + ((vcmax25_leaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
                gsvegsun[p - 1] = (gsvegsun[p - 1] + ((gs[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]))
                gsvegsha[p - 1] = (gsvegsha[p - 1] + ((gs[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]))
        windveg[p - 1] = 0.0
        windvegsun[p - 1] = 0.0
        windvegsha[p - 1] = 0.0
        tlveg[p - 1] = 0.0
        tlvegsun[p - 1] = 0.0
        tlvegsha[p - 1] = 0.0
        taveg[p - 1] = 0.0
        tavegsun[p - 1] = 0.0
        tavegsha[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                windveg[p - 1] = (windveg[p - 1] + ((wind[p - 1, ic - 1] * dpai[p - 1, ic - 1]) / ((laisun[p - 1] + laisha[p - 1]))))
                windvegsun[p - 1] = (windvegsun[p - 1] + (((wind[p - 1, ic - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) / laisun[p - 1]))
                windvegsha[p - 1] = (windvegsha[p - 1] + (((wind[p - 1, ic - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) / laisha[p - 1]))
                tlveg[p - 1] = (tlveg[p - 1] + ((tleaf_mean[p - 1, ic - 1] * dpai[p - 1, ic - 1]) / ((laisun[p - 1] + laisha[p - 1]))))
                tlvegsun[p - 1] = (tlvegsun[p - 1] + (((tleaf[p - 1, ic - 1, ISUN - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) / laisun[p - 1]))
                tlvegsha[p - 1] = (tlvegsha[p - 1] + (((tleaf[p - 1, ic - 1, ISHA - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) / laisha[p - 1]))
                taveg[p - 1] = (taveg[p - 1] + ((tair[p - 1, ic - 1] * dpai[p - 1, ic - 1]) / ((laisun[p - 1] + laisha[p - 1]))))
                tavegsun[p - 1] = (tavegsun[p - 1] + (((tair[p - 1, ic - 1] * fracsun[p - 1, ic - 1]) * dpai[p - 1, ic - 1]) / laisun[p - 1]))
                tavegsha[p - 1] = (tavegsha[p - 1] + (((tair[p - 1, ic - 1] * ((1.0 - fracsun[p - 1, ic - 1]))) * dpai[p - 1, ic - 1]) / laisha[p - 1]))
        minlwp = (-F_2P)
        fracminlwp[p - 1] = 0.0
        for ic in range(1, ncan[p - 1] + 1):
            if (dpai[p - 1, ic - 1] > 0.0):
                if (lwp_mean[p - 1, ic - 1] <= minlwp):
                    fracminlwp[p - 1] = (fracminlwp[p - 1] + dpai[p - 1, ic - 1])
        if (((lai[p - 1] + sai[p - 1])) > 0.0):
            fracminlwp[p - 1] = (fracminlwp[p - 1] / ((lai[p - 1] + sai[p - 1])))
    return mlcanopy_inst


# Flattened adapters for the differential gate (recast.transform.numpy.flat).
class _Record:
    def __init__(self, **fields):
        self.__dict__.update(fields)

def mlcanopyfluxes_flat(num_exposedvegp, filter_exposedvegp, np_, atm2lnd_inst__forc_lwrad_downscaled_col, atm2lnd_inst__forc_pbot_downscaled_col, atm2lnd_inst__forc_pco2_grc, atm2lnd_inst__forc_po2_grc, atm2lnd_inst__forc_solad_downscaled_col, atm2lnd_inst__forc_solai_grc, atm2lnd_inst__forc_t_downscaled_col, atm2lnd_inst__forc_u_grc, atm2lnd_inst__forc_v_grc, bounds__begp, bounds__endp, canopystate_inst__elai_patch, canopystate_inst__esai_patch, canopystate_inst__htop_patch, col__dz, col__nbedrock, col__snl, col__z, col__zi, energyflux_inst__eflx_lh_tot_patch, energyflux_inst__eflx_lwrad_out_patch, energyflux_inst__eflx_sh_tot_patch, energyflux_inst__taux_patch, energyflux_inst__tauy_patch, frictionvel_inst__forc_hgt_u_patch, frictionvel_inst__fv_patch, frictionvel_inst__u10_clm_patch, grc__latdeg, grc__londeg, mlcanopy_inst__ac_leaf, mlcanopy_inst__agross_leaf, mlcanopy_inst__aj_leaf, mlcanopy_inst__albcan_canopy, mlcanopy_inst__albsoib_soil, mlcanopy_inst__albsoid_soil, mlcanopy_inst__anet_leaf, mlcanopy_inst__ap_leaf, mlcanopy_inst__apar_leaf, mlcanopy_inst__apar_mean_profile, mlcanopy_inst__beta_canopy, mlcanopy_inst__btran_soil, mlcanopy_inst__cair_bef_profile, mlcanopy_inst__cair_profile, mlcanopy_inst__ceair_leaf, mlcanopy_inst__ci_leaf, mlcanopy_inst__co2ref_bef_forcing, mlcanopy_inst__co2ref_cur_forcing, mlcanopy_inst__co2ref_forcing, mlcanopy_inst__co2ref_next_forcing, mlcanopy_inst__cp_leaf, mlcanopy_inst__cpair_forcing, mlcanopy_inst__cpleaf_profile, mlcanopy_inst__cs_leaf, mlcanopy_inst__deair_profile, mlcanopy_inst__dh2ocan_profile, mlcanopy_inst__dlai_frac_profile, mlcanopy_inst__dlai_profile, mlcanopy_inst__dlwp_leaf, mlcanopy_inst__dpai_profile, mlcanopy_inst__dsai_frac_profile, mlcanopy_inst__dsai_profile, mlcanopy_inst__dtair_profile, mlcanopy_inst__dtg_soil, mlcanopy_inst__dtleaf_leaf, mlcanopy_inst__dz_profile, mlcanopy_inst__eair_bef_profile, mlcanopy_inst__eair_data_profile, mlcanopy_inst__eair_profile, mlcanopy_inst__eg_soil, mlcanopy_inst__eref_forcing, mlcanopy_inst__etair_profile, mlcanopy_inst__etflx_canopy, mlcanopy_inst__etleaf_mean_profile, mlcanopy_inst__etsoi_soil, mlcanopy_inst__etsrc_profile, mlcanopy_inst__etveg_canopy, mlcanopy_inst__etvegsha_canopy, mlcanopy_inst__etvegsun_canopy, mlcanopy_inst__evleaf_leaf, mlcanopy_inst__evleaf_mean_profile, mlcanopy_inst__evsrc_profile, mlcanopy_inst__evveg_canopy, mlcanopy_inst__fco2_mean_profile, mlcanopy_inst__fco2src_profile, mlcanopy_inst__fdry_profile, mlcanopy_inst__fracminlwp_canopy, mlcanopy_inst__fracsun_profile, mlcanopy_inst__fwet_profile, mlcanopy_inst__g0_canopy, mlcanopy_inst__g1_canopy, mlcanopy_inst__gac0_soil, mlcanopy_inst__gac_profile, mlcanopy_inst__gac_to_hc_canopy, mlcanopy_inst__gbc_leaf, mlcanopy_inst__gbh_leaf, mlcanopy_inst__gbv_leaf, mlcanopy_inst__gppveg_canopy, mlcanopy_inst__gppvegsha_canopy, mlcanopy_inst__gppvegsun_canopy, mlcanopy_inst__gs_leaf, mlcanopy_inst__gs_mean_profile, mlcanopy_inst__gsoi_soil, mlcanopy_inst__gspot_leaf, mlcanopy_inst__gsveg_canopy, mlcanopy_inst__gsvegsha_canopy, mlcanopy_inst__gsvegsun_canopy, mlcanopy_inst__h2ocan_bef_profile, mlcanopy_inst__h2ocan_profile, mlcanopy_inst__hs_leaf, mlcanopy_inst__je_leaf, mlcanopy_inst__jmax25_leaf, mlcanopy_inst__jmax25_profile, mlcanopy_inst__jmax_leaf, mlcanopy_inst__kb_profile, mlcanopy_inst__kc_eddy_profile, mlcanopy_inst__kc_leaf, mlcanopy_inst__ko_leaf, mlcanopy_inst__kp25_leaf, mlcanopy_inst__kp25_profile, mlcanopy_inst__kp_leaf, mlcanopy_inst__lai_canopy, mlcanopy_inst__laisha_canopy, mlcanopy_inst__laisun_canopy, mlcanopy_inst__lc_canopy, mlcanopy_inst__leaf_esat_leaf, mlcanopy_inst__lhflx_canopy, mlcanopy_inst__lhleaf_leaf, mlcanopy_inst__lhleaf_mean_profile, mlcanopy_inst__lhsoi_soil, mlcanopy_inst__lhsrc_profile, mlcanopy_inst__lhveg_canopy, mlcanopy_inst__lhvegsha_canopy, mlcanopy_inst__lhvegsun_canopy, mlcanopy_inst__lsc_profile, mlcanopy_inst__lwdwn_profile, mlcanopy_inst__lwleaf_leaf, mlcanopy_inst__lwleaf_mean_profile, mlcanopy_inst__lwp_bef_leaf, mlcanopy_inst__lwp_hist_leaf, mlcanopy_inst__lwp_leaf, mlcanopy_inst__lwp_mean_profile, mlcanopy_inst__lwsky_bef_forcing, mlcanopy_inst__lwsky_cur_forcing, mlcanopy_inst__lwsky_forcing, mlcanopy_inst__lwsky_next_forcing, mlcanopy_inst__lwsoi_soil, mlcanopy_inst__lwsrc_profile, mlcanopy_inst__lwup_canopy, mlcanopy_inst__lwupw_profile, mlcanopy_inst__lwveg_canopy, mlcanopy_inst__lwvegsha_canopy, mlcanopy_inst__lwvegsun_canopy, mlcanopy_inst__mflx_profile, mlcanopy_inst__mmair_forcing, mlcanopy_inst__nbot_canopy, mlcanopy_inst__ncan_canopy, mlcanopy_inst__ntop_canopy, mlcanopy_inst__o2ref_forcing, mlcanopy_inst__obu_canopy, mlcanopy_inst__pbeta_lai_canopy, mlcanopy_inst__pbeta_sai_canopy, mlcanopy_inst__pref_bef_forcing, mlcanopy_inst__pref_cur_forcing, mlcanopy_inst__pref_forcing, mlcanopy_inst__pref_next_forcing, mlcanopy_inst__prsc_canopy, mlcanopy_inst__psis_soil, mlcanopy_inst__qaf_canopy, mlcanopy_inst__qflx_intr_canopy, mlcanopy_inst__qflx_rain_forcing, mlcanopy_inst__qflx_snow_forcing, mlcanopy_inst__qflx_tflrain_canopy, mlcanopy_inst__qflx_tflsnow_canopy, mlcanopy_inst__qref_bef_forcing, mlcanopy_inst__qref_cur_forcing, mlcanopy_inst__qref_forcing, mlcanopy_inst__qref_next_forcing, mlcanopy_inst__rd25_leaf, mlcanopy_inst__rd25_profile, mlcanopy_inst__rd_leaf, mlcanopy_inst__rhg_soil, mlcanopy_inst__rhoair_forcing, mlcanopy_inst__rhomol_forcing, mlcanopy_inst__rnet_canopy, mlcanopy_inst__rnleaf_leaf, mlcanopy_inst__rnleaf_mean_profile, mlcanopy_inst__rnsoi_soil, mlcanopy_inst__rnsrc_profile, mlcanopy_inst__root_biomass_canopy, mlcanopy_inst__rsoil_soil, mlcanopy_inst__sai_canopy, mlcanopy_inst__shair_profile, mlcanopy_inst__shflx_canopy, mlcanopy_inst__shleaf_leaf, mlcanopy_inst__shleaf_mean_profile, mlcanopy_inst__shsoi_soil, mlcanopy_inst__shsrc_profile, mlcanopy_inst__shveg_canopy, mlcanopy_inst__shvegsha_canopy, mlcanopy_inst__shvegsun_canopy, mlcanopy_inst__soil_dz_soil, mlcanopy_inst__soil_et_loss_soil, mlcanopy_inst__soil_t_soil, mlcanopy_inst__soil_tk_soil, mlcanopy_inst__soilres_soil, mlcanopy_inst__solar_zen_forcing, mlcanopy_inst__stair_profile, mlcanopy_inst__stflx_air_canopy, mlcanopy_inst__stflx_veg_canopy, mlcanopy_inst__stleaf_leaf, mlcanopy_inst__stleaf_mean_profile, mlcanopy_inst__stsrc_profile, mlcanopy_inst__swbeam_profile, mlcanopy_inst__swdwn_profile, mlcanopy_inst__swleaf_leaf, mlcanopy_inst__swleaf_mean_profile, mlcanopy_inst__swskyb_bef_forcing, mlcanopy_inst__swskyb_cur_forcing, mlcanopy_inst__swskyb_forcing, mlcanopy_inst__swskyb_next_forcing, mlcanopy_inst__swskyd_bef_forcing, mlcanopy_inst__swskyd_cur_forcing, mlcanopy_inst__swskyd_forcing, mlcanopy_inst__swskyd_next_forcing, mlcanopy_inst__swsoi_soil, mlcanopy_inst__swsrc_profile, mlcanopy_inst__swupw_profile, mlcanopy_inst__swveg_canopy, mlcanopy_inst__swvegsha_canopy, mlcanopy_inst__swvegsun_canopy, mlcanopy_inst__tacclim_forcing, mlcanopy_inst__taf_canopy, mlcanopy_inst__tair_bef_profile, mlcanopy_inst__tair_data_profile, mlcanopy_inst__tair_profile, mlcanopy_inst__taveg_canopy, mlcanopy_inst__tavegsha_canopy, mlcanopy_inst__tavegsun_canopy, mlcanopy_inst__tb_profile, mlcanopy_inst__tbi_profile, mlcanopy_inst__td_profile, mlcanopy_inst__tg_bef_soil, mlcanopy_inst__tg_soil, mlcanopy_inst__thref_forcing, mlcanopy_inst__thvref_forcing, mlcanopy_inst__tleaf_bef_leaf, mlcanopy_inst__tleaf_hist_leaf, mlcanopy_inst__tleaf_leaf, mlcanopy_inst__tleaf_mean_profile, mlcanopy_inst__tlveg_canopy, mlcanopy_inst__tlvegsha_canopy, mlcanopy_inst__tlvegsun_canopy, mlcanopy_inst__tref_bef_forcing, mlcanopy_inst__tref_cur_forcing, mlcanopy_inst__tref_forcing, mlcanopy_inst__tref_next_forcing, mlcanopy_inst__trleaf_leaf, mlcanopy_inst__trleaf_mean_profile, mlcanopy_inst__trsrc_profile, mlcanopy_inst__trveg_canopy, mlcanopy_inst__uaf_canopy, mlcanopy_inst__uref_bef_forcing, mlcanopy_inst__uref_cur_forcing, mlcanopy_inst__uref_forcing, mlcanopy_inst__uref_next_forcing, mlcanopy_inst__ustar_canopy, mlcanopy_inst__vcmax25_leaf, mlcanopy_inst__vcmax25_profile, mlcanopy_inst__vcmax25sha_canopy, mlcanopy_inst__vcmax25sun_canopy, mlcanopy_inst__vcmax25veg_canopy, mlcanopy_inst__vcmax_leaf, mlcanopy_inst__vpd_leaf, mlcanopy_inst__wind_data_profile, mlcanopy_inst__wind_profile, mlcanopy_inst__windveg_canopy, mlcanopy_inst__windvegsha_canopy, mlcanopy_inst__windvegsun_canopy, mlcanopy_inst__z0m_canopy, mlcanopy_inst__zbot_canopy, mlcanopy_inst__zdisp_canopy, mlcanopy_inst__zref_forcing, mlcanopy_inst__zs_profile, mlcanopy_inst__ztop_canopy, mlcanopy_inst__zw_profile, mlpftcon__capac_spa, mlpftcon__clump_fac, mlpftcon__emleaf, mlpftcon__g0_bb, mlpftcon__g0_med, mlpftcon__g1_bb, mlpftcon__g1_med, mlpftcon__gplant_spa, mlpftcon__gsmin_spa, mlpftcon__iota_spa, mlpftcon__psi50_gs, mlpftcon__root_density_spa, mlpftcon__root_radius_spa, mlpftcon__root_resist_spa, mlpftcon__shape_gs, mlpftcon__vcmaxpft, patch__column, patch__gridcell, patch__itype, pftcon__c3psn, pftcon__dleaf, pftcon__rhol, pftcon__rhos, pftcon__slatop, pftcon__taul, pftcon__taus, pftcon__xl, soilstate_inst__hk_l_col, soilstate_inst__rootfr_patch, soilstate_inst__smp_l_col, soilstate_inst__soilresis_col, soilstate_inst__thk_col, solarabs_inst__fsa_patch, surfalb_inst__albd_patch, surfalb_inst__albgrd_col, surfalb_inst__albgri_col, surfalb_inst__albi_patch, temperature_inst__t_a10_patch, temperature_inst__t_ref2m_patch, temperature_inst__t_soisno_col, wateratm2lndbulk_inst__forc_q_downscaled_col, wateratm2lndbulk_inst__forc_rain_downscaled_col, wateratm2lndbulk_inst__forc_snow_downscaled_col, waterdiagnosticbulk_inst__q_ref2m_patch, waterfluxbulk_inst__qflx_evap_tot_patch, waterstatebulk_inst__h2osoi_ice_col, clm_time_manager__curr_date_ymd, clm_time_manager__dtstep, clm_time_manager__itim, clm_time_manager__start_date_tod, clm_time_manager__start_date_ymd, clm_varcon__cpliq, clm_varcon__denh2o, clm_varcon__grav, clm_varcon__hsub, clm_varcon__hvap, clm_varcon__sb, clm_varcon__vkc, clm_varorb__eccen, clm_varorb__lambm0, clm_varorb__mvelpp, clm_varorb__obliqr, clm_varpar__nlevgrnd, clm_varpar__nlevsno, clm_varpar__nlevsoi, mlclm_varcon__ah12, mlclm_varcon__beta_neutral_max, mlclm_varcon__c2, mlclm_varcon__cd, mlclm_varcon__chil_max, mlclm_varcon__chil_min, mlclm_varcon__colim_c3a, mlclm_varcon__colim_c4a, mlclm_varcon__colim_c4b, mlclm_varcon__cp25, mlclm_varcon__cpbio, mlclm_varcon__cpd, mlclm_varcon__cpha, mlclm_varcon__cpw, mlclm_varcon__cr, mlclm_varcon__dc0, mlclm_varcon__dewmx, mlclm_varcon__dh0, mlclm_varcon__dh2o_to_dco2, mlclm_varcon__dtlgridh, mlclm_varcon__dtlgridm, mlclm_varcon__dv0, mlclm_varcon__emg, mlclm_varcon__eta_max, mlclm_varcon__fcarbon, mlclm_varcon__fwater, mlclm_varcon__fwet_exponent, mlclm_varcon__gb_factor, mlclm_varcon__gbh_min, mlclm_varcon__interception_fraction, mlclm_varcon__j_to_umol, mlclm_varcon__jmax25_to_vcmax25_acclim, mlclm_varcon__jmax25_to_vcmax25_noacclim, mlclm_varcon__jmaxha_acclim, mlclm_varcon__jmaxha_noacclim, mlclm_varcon__jmaxhd_acclim, mlclm_varcon__jmaxhd_noacclim, mlclm_varcon__jmaxse_acclim, mlclm_varcon__jmaxse_noacclim, mlclm_varcon__kb_max, mlclm_varcon__kc25, mlclm_varcon__kcha, mlclm_varcon__ko25, mlclm_varcon__koha, mlclm_varcon__kp25_to_vcmax25_c4, mlclm_varcon__lapse_rate, mlclm_varcon__lcl_max, mlclm_varcon__lcl_min, mlclm_varcon__maximum_leaf_wetted_fraction, mlclm_varcon__mmdry, mlclm_varcon__mmh2o, mlclm_varcon__phi_psii, mlclm_varcon__pr0, mlclm_varcon__pr1, mlclm_varcon__pr2, mlclm_varcon__psigridh, mlclm_varcon__psigridm, mlclm_varcon__qe_c4, mlclm_varcon__ra_max, mlclm_varcon__rd25_to_vcmax25_c3, mlclm_varcon__rd25_to_vcmax25_c4, mlclm_varcon__rdha, mlclm_varcon__rdhd, mlclm_varcon__rdse, mlclm_varcon__rgas, mlclm_varcon__rh_min_bb, mlclm_varcon__theta_j, mlclm_varcon__vcmaxha_acclim, mlclm_varcon__vcmaxha_noacclim, mlclm_varcon__vcmaxhd_acclim, mlclm_varcon__vcmaxhd_noacclim, mlclm_varcon__vcmaxse_acclim, mlclm_varcon__vcmaxse_noacclim, mlclm_varcon__visc0, mlclm_varcon__vpd_min_med, mlclm_varcon__wind_forc_min, mlclm_varcon__z0mg, mlclm_varcon__zdtgridh, mlclm_varcon__zdtgridm, mlclm_varctl__acclim_type, mlclm_varctl__colim_type, mlclm_varctl__dpai_min, mlclm_varctl__dtime_ml, mlclm_varctl__dz_param, mlclm_varctl__dz_short, mlclm_varctl__dz_tall, mlclm_varctl__flux_profile_type, mlclm_varctl__gb_type, mlclm_varctl__gs_solver, mlclm_varctl__gs_type, mlclm_varctl__gspot_type, mlclm_varctl__hf_extension_type, mlclm_varctl__kn_val, mlclm_varctl__leaf_optics_type, mlclm_varctl__light_type, mlclm_varctl__longwave_type, mlclm_varctl__met_type, mlclm_varctl__ml_vert_init, mlclm_varctl__mlcan_to_clm, mlclm_varctl__nlayer_above, mlclm_varctl__nlayer_within, mlclm_varctl__sparse_canopy_type, mlclm_varctl__turb_type):
    atm2lnd_inst = _Record(forc_lwrad_downscaled_col=atm2lnd_inst__forc_lwrad_downscaled_col, forc_pbot_downscaled_col=atm2lnd_inst__forc_pbot_downscaled_col, forc_pco2_grc=atm2lnd_inst__forc_pco2_grc, forc_po2_grc=atm2lnd_inst__forc_po2_grc, forc_solad_downscaled_col=atm2lnd_inst__forc_solad_downscaled_col, forc_solai_grc=atm2lnd_inst__forc_solai_grc, forc_t_downscaled_col=atm2lnd_inst__forc_t_downscaled_col, forc_u_grc=atm2lnd_inst__forc_u_grc, forc_v_grc=atm2lnd_inst__forc_v_grc)
    bounds = _Record(begp=bounds__begp, endp=bounds__endp)
    canopystate_inst = _Record(elai_patch=canopystate_inst__elai_patch, esai_patch=canopystate_inst__esai_patch, htop_patch=canopystate_inst__htop_patch)
    import columntype_numpy as _columntype
    if not hasattr(getattr(_columntype, 'col', None), '__dict__'):
        _columntype.col = _Record()
    _columntype.col.dz = col__dz
    _columntype.col.nbedrock = col__nbedrock
    _columntype.col.snl = col__snl
    _columntype.col.z = col__z
    _columntype.col.zi = col__zi
    energyflux_inst = _Record(eflx_lh_tot_patch=energyflux_inst__eflx_lh_tot_patch, eflx_lwrad_out_patch=energyflux_inst__eflx_lwrad_out_patch, eflx_sh_tot_patch=energyflux_inst__eflx_sh_tot_patch, taux_patch=energyflux_inst__taux_patch, tauy_patch=energyflux_inst__tauy_patch)
    frictionvel_inst = _Record(forc_hgt_u_patch=frictionvel_inst__forc_hgt_u_patch, fv_patch=frictionvel_inst__fv_patch, u10_clm_patch=frictionvel_inst__u10_clm_patch)
    import gridcelltype_numpy as _gridcelltype
    if not hasattr(getattr(_gridcelltype, 'grc', None), '__dict__'):
        _gridcelltype.grc = _Record()
    _gridcelltype.grc.latdeg = grc__latdeg
    _gridcelltype.grc.londeg = grc__londeg
    mlcanopy_inst = _Record(ac_leaf=mlcanopy_inst__ac_leaf, agross_leaf=mlcanopy_inst__agross_leaf, aj_leaf=mlcanopy_inst__aj_leaf, albcan_canopy=mlcanopy_inst__albcan_canopy, albsoib_soil=mlcanopy_inst__albsoib_soil, albsoid_soil=mlcanopy_inst__albsoid_soil, anet_leaf=mlcanopy_inst__anet_leaf, ap_leaf=mlcanopy_inst__ap_leaf, apar_leaf=mlcanopy_inst__apar_leaf, apar_mean_profile=mlcanopy_inst__apar_mean_profile, beta_canopy=mlcanopy_inst__beta_canopy, btran_soil=mlcanopy_inst__btran_soil, cair_bef_profile=mlcanopy_inst__cair_bef_profile, cair_profile=mlcanopy_inst__cair_profile, ceair_leaf=mlcanopy_inst__ceair_leaf, ci_leaf=mlcanopy_inst__ci_leaf, co2ref_bef_forcing=mlcanopy_inst__co2ref_bef_forcing, co2ref_cur_forcing=mlcanopy_inst__co2ref_cur_forcing, co2ref_forcing=mlcanopy_inst__co2ref_forcing, co2ref_next_forcing=mlcanopy_inst__co2ref_next_forcing, cp_leaf=mlcanopy_inst__cp_leaf, cpair_forcing=mlcanopy_inst__cpair_forcing, cpleaf_profile=mlcanopy_inst__cpleaf_profile, cs_leaf=mlcanopy_inst__cs_leaf, deair_profile=mlcanopy_inst__deair_profile, dh2ocan_profile=mlcanopy_inst__dh2ocan_profile, dlai_frac_profile=mlcanopy_inst__dlai_frac_profile, dlai_profile=mlcanopy_inst__dlai_profile, dlwp_leaf=mlcanopy_inst__dlwp_leaf, dpai_profile=mlcanopy_inst__dpai_profile, dsai_frac_profile=mlcanopy_inst__dsai_frac_profile, dsai_profile=mlcanopy_inst__dsai_profile, dtair_profile=mlcanopy_inst__dtair_profile, dtg_soil=mlcanopy_inst__dtg_soil, dtleaf_leaf=mlcanopy_inst__dtleaf_leaf, dz_profile=mlcanopy_inst__dz_profile, eair_bef_profile=mlcanopy_inst__eair_bef_profile, eair_data_profile=mlcanopy_inst__eair_data_profile, eair_profile=mlcanopy_inst__eair_profile, eg_soil=mlcanopy_inst__eg_soil, eref_forcing=mlcanopy_inst__eref_forcing, etair_profile=mlcanopy_inst__etair_profile, etflx_canopy=mlcanopy_inst__etflx_canopy, etleaf_mean_profile=mlcanopy_inst__etleaf_mean_profile, etsoi_soil=mlcanopy_inst__etsoi_soil, etsrc_profile=mlcanopy_inst__etsrc_profile, etveg_canopy=mlcanopy_inst__etveg_canopy, etvegsha_canopy=mlcanopy_inst__etvegsha_canopy, etvegsun_canopy=mlcanopy_inst__etvegsun_canopy, evleaf_leaf=mlcanopy_inst__evleaf_leaf, evleaf_mean_profile=mlcanopy_inst__evleaf_mean_profile, evsrc_profile=mlcanopy_inst__evsrc_profile, evveg_canopy=mlcanopy_inst__evveg_canopy, fco2_mean_profile=mlcanopy_inst__fco2_mean_profile, fco2src_profile=mlcanopy_inst__fco2src_profile, fdry_profile=mlcanopy_inst__fdry_profile, fracminlwp_canopy=mlcanopy_inst__fracminlwp_canopy, fracsun_profile=mlcanopy_inst__fracsun_profile, fwet_profile=mlcanopy_inst__fwet_profile, g0_canopy=mlcanopy_inst__g0_canopy, g1_canopy=mlcanopy_inst__g1_canopy, gac0_soil=mlcanopy_inst__gac0_soil, gac_profile=mlcanopy_inst__gac_profile, gac_to_hc_canopy=mlcanopy_inst__gac_to_hc_canopy, gbc_leaf=mlcanopy_inst__gbc_leaf, gbh_leaf=mlcanopy_inst__gbh_leaf, gbv_leaf=mlcanopy_inst__gbv_leaf, gppveg_canopy=mlcanopy_inst__gppveg_canopy, gppvegsha_canopy=mlcanopy_inst__gppvegsha_canopy, gppvegsun_canopy=mlcanopy_inst__gppvegsun_canopy, gs_leaf=mlcanopy_inst__gs_leaf, gs_mean_profile=mlcanopy_inst__gs_mean_profile, gsoi_soil=mlcanopy_inst__gsoi_soil, gspot_leaf=mlcanopy_inst__gspot_leaf, gsveg_canopy=mlcanopy_inst__gsveg_canopy, gsvegsha_canopy=mlcanopy_inst__gsvegsha_canopy, gsvegsun_canopy=mlcanopy_inst__gsvegsun_canopy, h2ocan_bef_profile=mlcanopy_inst__h2ocan_bef_profile, h2ocan_profile=mlcanopy_inst__h2ocan_profile, hs_leaf=mlcanopy_inst__hs_leaf, je_leaf=mlcanopy_inst__je_leaf, jmax25_leaf=mlcanopy_inst__jmax25_leaf, jmax25_profile=mlcanopy_inst__jmax25_profile, jmax_leaf=mlcanopy_inst__jmax_leaf, kb_profile=mlcanopy_inst__kb_profile, kc_eddy_profile=mlcanopy_inst__kc_eddy_profile, kc_leaf=mlcanopy_inst__kc_leaf, ko_leaf=mlcanopy_inst__ko_leaf, kp25_leaf=mlcanopy_inst__kp25_leaf, kp25_profile=mlcanopy_inst__kp25_profile, kp_leaf=mlcanopy_inst__kp_leaf, lai_canopy=mlcanopy_inst__lai_canopy, laisha_canopy=mlcanopy_inst__laisha_canopy, laisun_canopy=mlcanopy_inst__laisun_canopy, lc_canopy=mlcanopy_inst__lc_canopy, leaf_esat_leaf=mlcanopy_inst__leaf_esat_leaf, lhflx_canopy=mlcanopy_inst__lhflx_canopy, lhleaf_leaf=mlcanopy_inst__lhleaf_leaf, lhleaf_mean_profile=mlcanopy_inst__lhleaf_mean_profile, lhsoi_soil=mlcanopy_inst__lhsoi_soil, lhsrc_profile=mlcanopy_inst__lhsrc_profile, lhveg_canopy=mlcanopy_inst__lhveg_canopy, lhvegsha_canopy=mlcanopy_inst__lhvegsha_canopy, lhvegsun_canopy=mlcanopy_inst__lhvegsun_canopy, lsc_profile=mlcanopy_inst__lsc_profile, lwdwn_profile=mlcanopy_inst__lwdwn_profile, lwleaf_leaf=mlcanopy_inst__lwleaf_leaf, lwleaf_mean_profile=mlcanopy_inst__lwleaf_mean_profile, lwp_bef_leaf=mlcanopy_inst__lwp_bef_leaf, lwp_hist_leaf=mlcanopy_inst__lwp_hist_leaf, lwp_leaf=mlcanopy_inst__lwp_leaf, lwp_mean_profile=mlcanopy_inst__lwp_mean_profile, lwsky_bef_forcing=mlcanopy_inst__lwsky_bef_forcing, lwsky_cur_forcing=mlcanopy_inst__lwsky_cur_forcing, lwsky_forcing=mlcanopy_inst__lwsky_forcing, lwsky_next_forcing=mlcanopy_inst__lwsky_next_forcing, lwsoi_soil=mlcanopy_inst__lwsoi_soil, lwsrc_profile=mlcanopy_inst__lwsrc_profile, lwup_canopy=mlcanopy_inst__lwup_canopy, lwupw_profile=mlcanopy_inst__lwupw_profile, lwveg_canopy=mlcanopy_inst__lwveg_canopy, lwvegsha_canopy=mlcanopy_inst__lwvegsha_canopy, lwvegsun_canopy=mlcanopy_inst__lwvegsun_canopy, mflx_profile=mlcanopy_inst__mflx_profile, mmair_forcing=mlcanopy_inst__mmair_forcing, nbot_canopy=mlcanopy_inst__nbot_canopy, ncan_canopy=mlcanopy_inst__ncan_canopy, ntop_canopy=mlcanopy_inst__ntop_canopy, o2ref_forcing=mlcanopy_inst__o2ref_forcing, obu_canopy=mlcanopy_inst__obu_canopy, pbeta_lai_canopy=mlcanopy_inst__pbeta_lai_canopy, pbeta_sai_canopy=mlcanopy_inst__pbeta_sai_canopy, pref_bef_forcing=mlcanopy_inst__pref_bef_forcing, pref_cur_forcing=mlcanopy_inst__pref_cur_forcing, pref_forcing=mlcanopy_inst__pref_forcing, pref_next_forcing=mlcanopy_inst__pref_next_forcing, prsc_canopy=mlcanopy_inst__prsc_canopy, psis_soil=mlcanopy_inst__psis_soil, qaf_canopy=mlcanopy_inst__qaf_canopy, qflx_intr_canopy=mlcanopy_inst__qflx_intr_canopy, qflx_rain_forcing=mlcanopy_inst__qflx_rain_forcing, qflx_snow_forcing=mlcanopy_inst__qflx_snow_forcing, qflx_tflrain_canopy=mlcanopy_inst__qflx_tflrain_canopy, qflx_tflsnow_canopy=mlcanopy_inst__qflx_tflsnow_canopy, qref_bef_forcing=mlcanopy_inst__qref_bef_forcing, qref_cur_forcing=mlcanopy_inst__qref_cur_forcing, qref_forcing=mlcanopy_inst__qref_forcing, qref_next_forcing=mlcanopy_inst__qref_next_forcing, rd25_leaf=mlcanopy_inst__rd25_leaf, rd25_profile=mlcanopy_inst__rd25_profile, rd_leaf=mlcanopy_inst__rd_leaf, rhg_soil=mlcanopy_inst__rhg_soil, rhoair_forcing=mlcanopy_inst__rhoair_forcing, rhomol_forcing=mlcanopy_inst__rhomol_forcing, rnet_canopy=mlcanopy_inst__rnet_canopy, rnleaf_leaf=mlcanopy_inst__rnleaf_leaf, rnleaf_mean_profile=mlcanopy_inst__rnleaf_mean_profile, rnsoi_soil=mlcanopy_inst__rnsoi_soil, rnsrc_profile=mlcanopy_inst__rnsrc_profile, root_biomass_canopy=mlcanopy_inst__root_biomass_canopy, rsoil_soil=mlcanopy_inst__rsoil_soil, sai_canopy=mlcanopy_inst__sai_canopy, shair_profile=mlcanopy_inst__shair_profile, shflx_canopy=mlcanopy_inst__shflx_canopy, shleaf_leaf=mlcanopy_inst__shleaf_leaf, shleaf_mean_profile=mlcanopy_inst__shleaf_mean_profile, shsoi_soil=mlcanopy_inst__shsoi_soil, shsrc_profile=mlcanopy_inst__shsrc_profile, shveg_canopy=mlcanopy_inst__shveg_canopy, shvegsha_canopy=mlcanopy_inst__shvegsha_canopy, shvegsun_canopy=mlcanopy_inst__shvegsun_canopy, soil_dz_soil=mlcanopy_inst__soil_dz_soil, soil_et_loss_soil=mlcanopy_inst__soil_et_loss_soil, soil_t_soil=mlcanopy_inst__soil_t_soil, soil_tk_soil=mlcanopy_inst__soil_tk_soil, soilres_soil=mlcanopy_inst__soilres_soil, solar_zen_forcing=mlcanopy_inst__solar_zen_forcing, stair_profile=mlcanopy_inst__stair_profile, stflx_air_canopy=mlcanopy_inst__stflx_air_canopy, stflx_veg_canopy=mlcanopy_inst__stflx_veg_canopy, stleaf_leaf=mlcanopy_inst__stleaf_leaf, stleaf_mean_profile=mlcanopy_inst__stleaf_mean_profile, stsrc_profile=mlcanopy_inst__stsrc_profile, swbeam_profile=mlcanopy_inst__swbeam_profile, swdwn_profile=mlcanopy_inst__swdwn_profile, swleaf_leaf=mlcanopy_inst__swleaf_leaf, swleaf_mean_profile=mlcanopy_inst__swleaf_mean_profile, swskyb_bef_forcing=mlcanopy_inst__swskyb_bef_forcing, swskyb_cur_forcing=mlcanopy_inst__swskyb_cur_forcing, swskyb_forcing=mlcanopy_inst__swskyb_forcing, swskyb_next_forcing=mlcanopy_inst__swskyb_next_forcing, swskyd_bef_forcing=mlcanopy_inst__swskyd_bef_forcing, swskyd_cur_forcing=mlcanopy_inst__swskyd_cur_forcing, swskyd_forcing=mlcanopy_inst__swskyd_forcing, swskyd_next_forcing=mlcanopy_inst__swskyd_next_forcing, swsoi_soil=mlcanopy_inst__swsoi_soil, swsrc_profile=mlcanopy_inst__swsrc_profile, swupw_profile=mlcanopy_inst__swupw_profile, swveg_canopy=mlcanopy_inst__swveg_canopy, swvegsha_canopy=mlcanopy_inst__swvegsha_canopy, swvegsun_canopy=mlcanopy_inst__swvegsun_canopy, tacclim_forcing=mlcanopy_inst__tacclim_forcing, taf_canopy=mlcanopy_inst__taf_canopy, tair_bef_profile=mlcanopy_inst__tair_bef_profile, tair_data_profile=mlcanopy_inst__tair_data_profile, tair_profile=mlcanopy_inst__tair_profile, taveg_canopy=mlcanopy_inst__taveg_canopy, tavegsha_canopy=mlcanopy_inst__tavegsha_canopy, tavegsun_canopy=mlcanopy_inst__tavegsun_canopy, tb_profile=mlcanopy_inst__tb_profile, tbi_profile=mlcanopy_inst__tbi_profile, td_profile=mlcanopy_inst__td_profile, tg_bef_soil=mlcanopy_inst__tg_bef_soil, tg_soil=mlcanopy_inst__tg_soil, thref_forcing=mlcanopy_inst__thref_forcing, thvref_forcing=mlcanopy_inst__thvref_forcing, tleaf_bef_leaf=mlcanopy_inst__tleaf_bef_leaf, tleaf_hist_leaf=mlcanopy_inst__tleaf_hist_leaf, tleaf_leaf=mlcanopy_inst__tleaf_leaf, tleaf_mean_profile=mlcanopy_inst__tleaf_mean_profile, tlveg_canopy=mlcanopy_inst__tlveg_canopy, tlvegsha_canopy=mlcanopy_inst__tlvegsha_canopy, tlvegsun_canopy=mlcanopy_inst__tlvegsun_canopy, tref_bef_forcing=mlcanopy_inst__tref_bef_forcing, tref_cur_forcing=mlcanopy_inst__tref_cur_forcing, tref_forcing=mlcanopy_inst__tref_forcing, tref_next_forcing=mlcanopy_inst__tref_next_forcing, trleaf_leaf=mlcanopy_inst__trleaf_leaf, trleaf_mean_profile=mlcanopy_inst__trleaf_mean_profile, trsrc_profile=mlcanopy_inst__trsrc_profile, trveg_canopy=mlcanopy_inst__trveg_canopy, uaf_canopy=mlcanopy_inst__uaf_canopy, uref_bef_forcing=mlcanopy_inst__uref_bef_forcing, uref_cur_forcing=mlcanopy_inst__uref_cur_forcing, uref_forcing=mlcanopy_inst__uref_forcing, uref_next_forcing=mlcanopy_inst__uref_next_forcing, ustar_canopy=mlcanopy_inst__ustar_canopy, vcmax25_leaf=mlcanopy_inst__vcmax25_leaf, vcmax25_profile=mlcanopy_inst__vcmax25_profile, vcmax25sha_canopy=mlcanopy_inst__vcmax25sha_canopy, vcmax25sun_canopy=mlcanopy_inst__vcmax25sun_canopy, vcmax25veg_canopy=mlcanopy_inst__vcmax25veg_canopy, vcmax_leaf=mlcanopy_inst__vcmax_leaf, vpd_leaf=mlcanopy_inst__vpd_leaf, wind_data_profile=mlcanopy_inst__wind_data_profile, wind_profile=mlcanopy_inst__wind_profile, windveg_canopy=mlcanopy_inst__windveg_canopy, windvegsha_canopy=mlcanopy_inst__windvegsha_canopy, windvegsun_canopy=mlcanopy_inst__windvegsun_canopy, z0m_canopy=mlcanopy_inst__z0m_canopy, zbot_canopy=mlcanopy_inst__zbot_canopy, zdisp_canopy=mlcanopy_inst__zdisp_canopy, zref_forcing=mlcanopy_inst__zref_forcing, zs_profile=mlcanopy_inst__zs_profile, ztop_canopy=mlcanopy_inst__ztop_canopy, zw_profile=mlcanopy_inst__zw_profile)
    import mlpftconmod_numpy as _mlpftconmod
    if not hasattr(getattr(_mlpftconmod, 'mlpftcon', None), '__dict__'):
        _mlpftconmod.mlpftcon = _Record()
    _mlpftconmod.mlpftcon.capac_spa = mlpftcon__capac_spa
    _mlpftconmod.mlpftcon.clump_fac = mlpftcon__clump_fac
    _mlpftconmod.mlpftcon.emleaf = mlpftcon__emleaf
    _mlpftconmod.mlpftcon.g0_bb = mlpftcon__g0_bb
    _mlpftconmod.mlpftcon.g0_med = mlpftcon__g0_med
    _mlpftconmod.mlpftcon.g1_bb = mlpftcon__g1_bb
    _mlpftconmod.mlpftcon.g1_med = mlpftcon__g1_med
    _mlpftconmod.mlpftcon.gplant_spa = mlpftcon__gplant_spa
    _mlpftconmod.mlpftcon.gsmin_spa = mlpftcon__gsmin_spa
    _mlpftconmod.mlpftcon.iota_spa = mlpftcon__iota_spa
    _mlpftconmod.mlpftcon.psi50_gs = mlpftcon__psi50_gs
    _mlpftconmod.mlpftcon.root_density_spa = mlpftcon__root_density_spa
    _mlpftconmod.mlpftcon.root_radius_spa = mlpftcon__root_radius_spa
    _mlpftconmod.mlpftcon.root_resist_spa = mlpftcon__root_resist_spa
    _mlpftconmod.mlpftcon.shape_gs = mlpftcon__shape_gs
    _mlpftconmod.mlpftcon.vcmaxpft = mlpftcon__vcmaxpft
    import patchtype_numpy as _patchtype
    if not hasattr(getattr(_patchtype, 'patch', None), '__dict__'):
        _patchtype.patch = _Record()
    _patchtype.patch.column = patch__column
    _patchtype.patch.gridcell = patch__gridcell
    _patchtype.patch.itype = patch__itype
    import pftconmod_numpy as _pftconmod
    if not hasattr(getattr(_pftconmod, 'pftcon', None), '__dict__'):
        _pftconmod.pftcon = _Record()
    _pftconmod.pftcon.c3psn = pftcon__c3psn
    _pftconmod.pftcon.dleaf = pftcon__dleaf
    _pftconmod.pftcon.rhol = pftcon__rhol
    _pftconmod.pftcon.rhos = pftcon__rhos
    _pftconmod.pftcon.slatop = pftcon__slatop
    _pftconmod.pftcon.taul = pftcon__taul
    _pftconmod.pftcon.taus = pftcon__taus
    _pftconmod.pftcon.xl = pftcon__xl
    soilstate_inst = _Record(hk_l_col=soilstate_inst__hk_l_col, rootfr_patch=soilstate_inst__rootfr_patch, smp_l_col=soilstate_inst__smp_l_col, soilresis_col=soilstate_inst__soilresis_col, thk_col=soilstate_inst__thk_col)
    solarabs_inst = _Record(fsa_patch=solarabs_inst__fsa_patch)
    surfalb_inst = _Record(albd_patch=surfalb_inst__albd_patch, albgrd_col=surfalb_inst__albgrd_col, albgri_col=surfalb_inst__albgri_col, albi_patch=surfalb_inst__albi_patch)
    temperature_inst = _Record(t_a10_patch=temperature_inst__t_a10_patch, t_ref2m_patch=temperature_inst__t_ref2m_patch, t_soisno_col=temperature_inst__t_soisno_col)
    wateratm2lndbulk_inst = _Record(forc_q_downscaled_col=wateratm2lndbulk_inst__forc_q_downscaled_col, forc_rain_downscaled_col=wateratm2lndbulk_inst__forc_rain_downscaled_col, forc_snow_downscaled_col=wateratm2lndbulk_inst__forc_snow_downscaled_col)
    waterdiagnosticbulk_inst = _Record(q_ref2m_patch=waterdiagnosticbulk_inst__q_ref2m_patch)
    waterfluxbulk_inst = _Record(qflx_evap_tot_patch=waterfluxbulk_inst__qflx_evap_tot_patch)
    waterstatebulk_inst = _Record(h2osoi_ice_col=waterstatebulk_inst__h2osoi_ice_col)
    import clm_time_manager_numpy as _clm_time_manager
    _clm_time_manager.curr_date_ymd = clm_time_manager__curr_date_ymd
    import clm_time_manager_numpy as _clm_time_manager
    _clm_time_manager.dtstep = clm_time_manager__dtstep
    import clm_time_manager_numpy as _clm_time_manager
    _clm_time_manager.itim = clm_time_manager__itim
    import clm_time_manager_numpy as _clm_time_manager
    _clm_time_manager.start_date_tod = clm_time_manager__start_date_tod
    import clm_time_manager_numpy as _clm_time_manager
    _clm_time_manager.start_date_ymd = clm_time_manager__start_date_ymd
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.cpliq = clm_varcon__cpliq
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.denh2o = clm_varcon__denh2o
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.grav = clm_varcon__grav
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.hsub = clm_varcon__hsub
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.hvap = clm_varcon__hvap
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.sb = clm_varcon__sb
    import clm_varcon_numpy as _clm_varcon
    _clm_varcon.vkc = clm_varcon__vkc
    import clm_varorb_numpy as _clm_varorb
    _clm_varorb.eccen = clm_varorb__eccen
    import clm_varorb_numpy as _clm_varorb
    _clm_varorb.lambm0 = clm_varorb__lambm0
    import clm_varorb_numpy as _clm_varorb
    _clm_varorb.mvelpp = clm_varorb__mvelpp
    import clm_varorb_numpy as _clm_varorb
    _clm_varorb.obliqr = clm_varorb__obliqr
    import clm_varpar_numpy as _clm_varpar
    _clm_varpar.nlevgrnd = clm_varpar__nlevgrnd
    import clm_varpar_numpy as _clm_varpar
    _clm_varpar.nlevsno = clm_varpar__nlevsno
    import clm_varpar_numpy as _clm_varpar
    _clm_varpar.nlevsoi = clm_varpar__nlevsoi
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.ah12 = mlclm_varcon__ah12
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.beta_neutral_max = mlclm_varcon__beta_neutral_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.c2 = mlclm_varcon__c2
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cd = mlclm_varcon__cd
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.chil_max = mlclm_varcon__chil_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.chil_min = mlclm_varcon__chil_min
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.colim_c3a = mlclm_varcon__colim_c3a
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.colim_c4a = mlclm_varcon__colim_c4a
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.colim_c4b = mlclm_varcon__colim_c4b
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cp25 = mlclm_varcon__cp25
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cpbio = mlclm_varcon__cpbio
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cpd = mlclm_varcon__cpd
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cpha = mlclm_varcon__cpha
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cpw = mlclm_varcon__cpw
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.cr = mlclm_varcon__cr
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dc0 = mlclm_varcon__dc0
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dewmx = mlclm_varcon__dewmx
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dh0 = mlclm_varcon__dh0
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dh2o_to_dco2 = mlclm_varcon__dh2o_to_dco2
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dtlgridh = mlclm_varcon__dtlgridh
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dtlgridm = mlclm_varcon__dtlgridm
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.dv0 = mlclm_varcon__dv0
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.emg = mlclm_varcon__emg
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.eta_max = mlclm_varcon__eta_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.fcarbon = mlclm_varcon__fcarbon
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.fwater = mlclm_varcon__fwater
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.fwet_exponent = mlclm_varcon__fwet_exponent
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.gb_factor = mlclm_varcon__gb_factor
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.gbh_min = mlclm_varcon__gbh_min
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.interception_fraction = mlclm_varcon__interception_fraction
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.j_to_umol = mlclm_varcon__j_to_umol
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmax25_to_vcmax25_acclim = mlclm_varcon__jmax25_to_vcmax25_acclim
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.jmax25_to_vcmax25_noacclim = mlclm_varcon__jmax25_to_vcmax25_noacclim
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
    _mlclm_varcon.kb_max = mlclm_varcon__kb_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.kc25 = mlclm_varcon__kc25
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.kcha = mlclm_varcon__kcha
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.ko25 = mlclm_varcon__ko25
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.koha = mlclm_varcon__koha
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.kp25_to_vcmax25_c4 = mlclm_varcon__kp25_to_vcmax25_c4
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.lapse_rate = mlclm_varcon__lapse_rate
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.lcl_max = mlclm_varcon__lcl_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.lcl_min = mlclm_varcon__lcl_min
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.maximum_leaf_wetted_fraction = mlclm_varcon__maximum_leaf_wetted_fraction
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.mmdry = mlclm_varcon__mmdry
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.mmh2o = mlclm_varcon__mmh2o
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.phi_psii = mlclm_varcon__phi_psii
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
    _mlclm_varcon.qe_c4 = mlclm_varcon__qe_c4
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.ra_max = mlclm_varcon__ra_max
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.rd25_to_vcmax25_c3 = mlclm_varcon__rd25_to_vcmax25_c3
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.rd25_to_vcmax25_c4 = mlclm_varcon__rd25_to_vcmax25_c4
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
    _mlclm_varcon.visc0 = mlclm_varcon__visc0
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.vpd_min_med = mlclm_varcon__vpd_min_med
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.wind_forc_min = mlclm_varcon__wind_forc_min
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.z0mg = mlclm_varcon__z0mg
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.zdtgridh = mlclm_varcon__zdtgridh
    import mlclm_varcon_numpy as _mlclm_varcon
    _mlclm_varcon.zdtgridm = mlclm_varcon__zdtgridm
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.acclim_type = mlclm_varctl__acclim_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.colim_type = mlclm_varctl__colim_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.dpai_min = mlclm_varctl__dpai_min
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.dtime_ml = mlclm_varctl__dtime_ml
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.dz_param = mlclm_varctl__dz_param
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.dz_short = mlclm_varctl__dz_short
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.dz_tall = mlclm_varctl__dz_tall
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.flux_profile_type = mlclm_varctl__flux_profile_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.gb_type = mlclm_varctl__gb_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.gs_solver = mlclm_varctl__gs_solver
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.gs_type = mlclm_varctl__gs_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.gspot_type = mlclm_varctl__gspot_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.hf_extension_type = mlclm_varctl__hf_extension_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.kn_val = mlclm_varctl__kn_val
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.leaf_optics_type = mlclm_varctl__leaf_optics_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.light_type = mlclm_varctl__light_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.longwave_type = mlclm_varctl__longwave_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.met_type = mlclm_varctl__met_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.ml_vert_init = mlclm_varctl__ml_vert_init
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.mlcan_to_clm = mlclm_varctl__mlcan_to_clm
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.nlayer_above = mlclm_varctl__nlayer_above
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.nlayer_within = mlclm_varctl__nlayer_within
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.sparse_canopy_type = mlclm_varctl__sparse_canopy_type
    import mlclm_varctl_numpy as _mlclm_varctl
    _mlclm_varctl.turb_type = mlclm_varctl__turb_type
    _out = mlcanopyfluxes(bounds=bounds, num_exposedvegp=num_exposedvegp, filter_exposedvegp=filter_exposedvegp, atm2lnd_inst=atm2lnd_inst, canopystate_inst=canopystate_inst, soilstate_inst=soilstate_inst, temperature_inst=temperature_inst, waterstatebulk_inst=waterstatebulk_inst, waterfluxbulk_inst=waterfluxbulk_inst, energyflux_inst=energyflux_inst, frictionvel_inst=frictionvel_inst, surfalb_inst=surfalb_inst, solarabs_inst=solarabs_inst, mlcanopy_inst=mlcanopy_inst, wateratm2lndbulk_inst=wateratm2lndbulk_inst, waterdiagnosticbulk_inst=waterdiagnosticbulk_inst)
    canopystate_inst_, soilstate_inst_, temperature_inst_, waterstatebulk_inst_, waterfluxbulk_inst_, energyflux_inst_, frictionvel_inst_, surfalb_inst_, solarabs_inst_, mlcanopy_inst_, waterdiagnosticbulk_inst_, = _out
    energyflux_inst__eflx_lh_tot_patch = energyflux_inst.eflx_lh_tot_patch
    energyflux_inst__eflx_lwrad_out_patch = energyflux_inst.eflx_lwrad_out_patch
    energyflux_inst__eflx_sh_tot_patch = energyflux_inst.eflx_sh_tot_patch
    energyflux_inst__taux_patch = energyflux_inst.taux_patch
    energyflux_inst__tauy_patch = energyflux_inst.tauy_patch
    frictionvel_inst__fv_patch = frictionvel_inst.fv_patch
    frictionvel_inst__u10_clm_patch = frictionvel_inst.u10_clm_patch
    mlcanopy_inst__ac_leaf = mlcanopy_inst.ac_leaf
    mlcanopy_inst__agross_leaf = mlcanopy_inst.agross_leaf
    mlcanopy_inst__aj_leaf = mlcanopy_inst.aj_leaf
    mlcanopy_inst__albcan_canopy = mlcanopy_inst.albcan_canopy
    mlcanopy_inst__albsoib_soil = mlcanopy_inst.albsoib_soil
    mlcanopy_inst__albsoid_soil = mlcanopy_inst.albsoid_soil
    mlcanopy_inst__anet_leaf = mlcanopy_inst.anet_leaf
    mlcanopy_inst__ap_leaf = mlcanopy_inst.ap_leaf
    mlcanopy_inst__apar_leaf = mlcanopy_inst.apar_leaf
    mlcanopy_inst__apar_mean_profile = mlcanopy_inst.apar_mean_profile
    mlcanopy_inst__beta_canopy = mlcanopy_inst.beta_canopy
    mlcanopy_inst__btran_soil = mlcanopy_inst.btran_soil
    mlcanopy_inst__cair_bef_profile = mlcanopy_inst.cair_bef_profile
    mlcanopy_inst__cair_profile = mlcanopy_inst.cair_profile
    mlcanopy_inst__ceair_leaf = mlcanopy_inst.ceair_leaf
    mlcanopy_inst__ci_leaf = mlcanopy_inst.ci_leaf
    mlcanopy_inst__co2ref_bef_forcing = mlcanopy_inst.co2ref_bef_forcing
    mlcanopy_inst__co2ref_cur_forcing = mlcanopy_inst.co2ref_cur_forcing
    mlcanopy_inst__co2ref_forcing = mlcanopy_inst.co2ref_forcing
    mlcanopy_inst__cp_leaf = mlcanopy_inst.cp_leaf
    mlcanopy_inst__cpair_forcing = mlcanopy_inst.cpair_forcing
    mlcanopy_inst__cpleaf_profile = mlcanopy_inst.cpleaf_profile
    mlcanopy_inst__cs_leaf = mlcanopy_inst.cs_leaf
    mlcanopy_inst__deair_profile = mlcanopy_inst.deair_profile
    mlcanopy_inst__dh2ocan_profile = mlcanopy_inst.dh2ocan_profile
    mlcanopy_inst__dlai_frac_profile = mlcanopy_inst.dlai_frac_profile
    mlcanopy_inst__dlai_profile = mlcanopy_inst.dlai_profile
    mlcanopy_inst__dlwp_leaf = mlcanopy_inst.dlwp_leaf
    mlcanopy_inst__dpai_profile = mlcanopy_inst.dpai_profile
    mlcanopy_inst__dsai_frac_profile = mlcanopy_inst.dsai_frac_profile
    mlcanopy_inst__dsai_profile = mlcanopy_inst.dsai_profile
    mlcanopy_inst__dtair_profile = mlcanopy_inst.dtair_profile
    mlcanopy_inst__dtg_soil = mlcanopy_inst.dtg_soil
    mlcanopy_inst__dtleaf_leaf = mlcanopy_inst.dtleaf_leaf
    mlcanopy_inst__dz_profile = mlcanopy_inst.dz_profile
    mlcanopy_inst__eair_bef_profile = mlcanopy_inst.eair_bef_profile
    mlcanopy_inst__eair_profile = mlcanopy_inst.eair_profile
    mlcanopy_inst__eg_soil = mlcanopy_inst.eg_soil
    mlcanopy_inst__eref_forcing = mlcanopy_inst.eref_forcing
    mlcanopy_inst__etair_profile = mlcanopy_inst.etair_profile
    mlcanopy_inst__etflx_canopy = mlcanopy_inst.etflx_canopy
    mlcanopy_inst__etleaf_mean_profile = mlcanopy_inst.etleaf_mean_profile
    mlcanopy_inst__etsoi_soil = mlcanopy_inst.etsoi_soil
    mlcanopy_inst__etsrc_profile = mlcanopy_inst.etsrc_profile
    mlcanopy_inst__etveg_canopy = mlcanopy_inst.etveg_canopy
    mlcanopy_inst__etvegsha_canopy = mlcanopy_inst.etvegsha_canopy
    mlcanopy_inst__etvegsun_canopy = mlcanopy_inst.etvegsun_canopy
    mlcanopy_inst__evleaf_leaf = mlcanopy_inst.evleaf_leaf
    mlcanopy_inst__evleaf_mean_profile = mlcanopy_inst.evleaf_mean_profile
    mlcanopy_inst__evsrc_profile = mlcanopy_inst.evsrc_profile
    mlcanopy_inst__evveg_canopy = mlcanopy_inst.evveg_canopy
    mlcanopy_inst__fco2_mean_profile = mlcanopy_inst.fco2_mean_profile
    mlcanopy_inst__fco2src_profile = mlcanopy_inst.fco2src_profile
    mlcanopy_inst__fdry_profile = mlcanopy_inst.fdry_profile
    mlcanopy_inst__fracminlwp_canopy = mlcanopy_inst.fracminlwp_canopy
    mlcanopy_inst__fracsun_profile = mlcanopy_inst.fracsun_profile
    mlcanopy_inst__fwet_profile = mlcanopy_inst.fwet_profile
    mlcanopy_inst__g0_canopy = mlcanopy_inst.g0_canopy
    mlcanopy_inst__g1_canopy = mlcanopy_inst.g1_canopy
    mlcanopy_inst__gac0_soil = mlcanopy_inst.gac0_soil
    mlcanopy_inst__gac_profile = mlcanopy_inst.gac_profile
    mlcanopy_inst__gac_to_hc_canopy = mlcanopy_inst.gac_to_hc_canopy
    mlcanopy_inst__gbc_leaf = mlcanopy_inst.gbc_leaf
    mlcanopy_inst__gbh_leaf = mlcanopy_inst.gbh_leaf
    mlcanopy_inst__gbv_leaf = mlcanopy_inst.gbv_leaf
    mlcanopy_inst__gppveg_canopy = mlcanopy_inst.gppveg_canopy
    mlcanopy_inst__gppvegsha_canopy = mlcanopy_inst.gppvegsha_canopy
    mlcanopy_inst__gppvegsun_canopy = mlcanopy_inst.gppvegsun_canopy
    mlcanopy_inst__gs_leaf = mlcanopy_inst.gs_leaf
    mlcanopy_inst__gs_mean_profile = mlcanopy_inst.gs_mean_profile
    mlcanopy_inst__gsoi_soil = mlcanopy_inst.gsoi_soil
    mlcanopy_inst__gspot_leaf = mlcanopy_inst.gspot_leaf
    mlcanopy_inst__gsveg_canopy = mlcanopy_inst.gsveg_canopy
    mlcanopy_inst__gsvegsha_canopy = mlcanopy_inst.gsvegsha_canopy
    mlcanopy_inst__gsvegsun_canopy = mlcanopy_inst.gsvegsun_canopy
    mlcanopy_inst__h2ocan_bef_profile = mlcanopy_inst.h2ocan_bef_profile
    mlcanopy_inst__h2ocan_profile = mlcanopy_inst.h2ocan_profile
    mlcanopy_inst__hs_leaf = mlcanopy_inst.hs_leaf
    mlcanopy_inst__je_leaf = mlcanopy_inst.je_leaf
    mlcanopy_inst__jmax25_leaf = mlcanopy_inst.jmax25_leaf
    mlcanopy_inst__jmax25_profile = mlcanopy_inst.jmax25_profile
    mlcanopy_inst__jmax_leaf = mlcanopy_inst.jmax_leaf
    mlcanopy_inst__kb_profile = mlcanopy_inst.kb_profile
    mlcanopy_inst__kc_eddy_profile = mlcanopy_inst.kc_eddy_profile
    mlcanopy_inst__kc_leaf = mlcanopy_inst.kc_leaf
    mlcanopy_inst__ko_leaf = mlcanopy_inst.ko_leaf
    mlcanopy_inst__kp25_leaf = mlcanopy_inst.kp25_leaf
    mlcanopy_inst__kp25_profile = mlcanopy_inst.kp25_profile
    mlcanopy_inst__kp_leaf = mlcanopy_inst.kp_leaf
    mlcanopy_inst__lai_canopy = mlcanopy_inst.lai_canopy
    mlcanopy_inst__laisha_canopy = mlcanopy_inst.laisha_canopy
    mlcanopy_inst__laisun_canopy = mlcanopy_inst.laisun_canopy
    mlcanopy_inst__lc_canopy = mlcanopy_inst.lc_canopy
    mlcanopy_inst__leaf_esat_leaf = mlcanopy_inst.leaf_esat_leaf
    mlcanopy_inst__lhflx_canopy = mlcanopy_inst.lhflx_canopy
    mlcanopy_inst__lhleaf_leaf = mlcanopy_inst.lhleaf_leaf
    mlcanopy_inst__lhleaf_mean_profile = mlcanopy_inst.lhleaf_mean_profile
    mlcanopy_inst__lhsoi_soil = mlcanopy_inst.lhsoi_soil
    mlcanopy_inst__lhsrc_profile = mlcanopy_inst.lhsrc_profile
    mlcanopy_inst__lhveg_canopy = mlcanopy_inst.lhveg_canopy
    mlcanopy_inst__lhvegsha_canopy = mlcanopy_inst.lhvegsha_canopy
    mlcanopy_inst__lhvegsun_canopy = mlcanopy_inst.lhvegsun_canopy
    mlcanopy_inst__lsc_profile = mlcanopy_inst.lsc_profile
    mlcanopy_inst__lwdwn_profile = mlcanopy_inst.lwdwn_profile
    mlcanopy_inst__lwleaf_leaf = mlcanopy_inst.lwleaf_leaf
    mlcanopy_inst__lwleaf_mean_profile = mlcanopy_inst.lwleaf_mean_profile
    mlcanopy_inst__lwp_bef_leaf = mlcanopy_inst.lwp_bef_leaf
    mlcanopy_inst__lwp_hist_leaf = mlcanopy_inst.lwp_hist_leaf
    mlcanopy_inst__lwp_leaf = mlcanopy_inst.lwp_leaf
    mlcanopy_inst__lwp_mean_profile = mlcanopy_inst.lwp_mean_profile
    mlcanopy_inst__lwsky_bef_forcing = mlcanopy_inst.lwsky_bef_forcing
    mlcanopy_inst__lwsky_cur_forcing = mlcanopy_inst.lwsky_cur_forcing
    mlcanopy_inst__lwsky_forcing = mlcanopy_inst.lwsky_forcing
    mlcanopy_inst__lwsoi_soil = mlcanopy_inst.lwsoi_soil
    mlcanopy_inst__lwsrc_profile = mlcanopy_inst.lwsrc_profile
    mlcanopy_inst__lwup_canopy = mlcanopy_inst.lwup_canopy
    mlcanopy_inst__lwupw_profile = mlcanopy_inst.lwupw_profile
    mlcanopy_inst__lwveg_canopy = mlcanopy_inst.lwveg_canopy
    mlcanopy_inst__lwvegsha_canopy = mlcanopy_inst.lwvegsha_canopy
    mlcanopy_inst__lwvegsun_canopy = mlcanopy_inst.lwvegsun_canopy
    mlcanopy_inst__mflx_profile = mlcanopy_inst.mflx_profile
    mlcanopy_inst__mmair_forcing = mlcanopy_inst.mmair_forcing
    mlcanopy_inst__nbot_canopy = mlcanopy_inst.nbot_canopy
    mlcanopy_inst__ncan_canopy = mlcanopy_inst.ncan_canopy
    mlcanopy_inst__ntop_canopy = mlcanopy_inst.ntop_canopy
    mlcanopy_inst__o2ref_forcing = mlcanopy_inst.o2ref_forcing
    mlcanopy_inst__obu_canopy = mlcanopy_inst.obu_canopy
    mlcanopy_inst__pbeta_lai_canopy = mlcanopy_inst.pbeta_lai_canopy
    mlcanopy_inst__pbeta_sai_canopy = mlcanopy_inst.pbeta_sai_canopy
    mlcanopy_inst__pref_bef_forcing = mlcanopy_inst.pref_bef_forcing
    mlcanopy_inst__pref_cur_forcing = mlcanopy_inst.pref_cur_forcing
    mlcanopy_inst__pref_forcing = mlcanopy_inst.pref_forcing
    mlcanopy_inst__prsc_canopy = mlcanopy_inst.prsc_canopy
    mlcanopy_inst__psis_soil = mlcanopy_inst.psis_soil
    mlcanopy_inst__qaf_canopy = mlcanopy_inst.qaf_canopy
    mlcanopy_inst__qflx_intr_canopy = mlcanopy_inst.qflx_intr_canopy
    mlcanopy_inst__qflx_rain_forcing = mlcanopy_inst.qflx_rain_forcing
    mlcanopy_inst__qflx_snow_forcing = mlcanopy_inst.qflx_snow_forcing
    mlcanopy_inst__qflx_tflrain_canopy = mlcanopy_inst.qflx_tflrain_canopy
    mlcanopy_inst__qflx_tflsnow_canopy = mlcanopy_inst.qflx_tflsnow_canopy
    mlcanopy_inst__qref_bef_forcing = mlcanopy_inst.qref_bef_forcing
    mlcanopy_inst__qref_cur_forcing = mlcanopy_inst.qref_cur_forcing
    mlcanopy_inst__qref_forcing = mlcanopy_inst.qref_forcing
    mlcanopy_inst__rd25_leaf = mlcanopy_inst.rd25_leaf
    mlcanopy_inst__rd25_profile = mlcanopy_inst.rd25_profile
    mlcanopy_inst__rd_leaf = mlcanopy_inst.rd_leaf
    mlcanopy_inst__rhg_soil = mlcanopy_inst.rhg_soil
    mlcanopy_inst__rhoair_forcing = mlcanopy_inst.rhoair_forcing
    mlcanopy_inst__rhomol_forcing = mlcanopy_inst.rhomol_forcing
    mlcanopy_inst__rnet_canopy = mlcanopy_inst.rnet_canopy
    mlcanopy_inst__rnleaf_leaf = mlcanopy_inst.rnleaf_leaf
    mlcanopy_inst__rnleaf_mean_profile = mlcanopy_inst.rnleaf_mean_profile
    mlcanopy_inst__rnsoi_soil = mlcanopy_inst.rnsoi_soil
    mlcanopy_inst__rnsrc_profile = mlcanopy_inst.rnsrc_profile
    mlcanopy_inst__rsoil_soil = mlcanopy_inst.rsoil_soil
    mlcanopy_inst__sai_canopy = mlcanopy_inst.sai_canopy
    mlcanopy_inst__shair_profile = mlcanopy_inst.shair_profile
    mlcanopy_inst__shflx_canopy = mlcanopy_inst.shflx_canopy
    mlcanopy_inst__shleaf_leaf = mlcanopy_inst.shleaf_leaf
    mlcanopy_inst__shleaf_mean_profile = mlcanopy_inst.shleaf_mean_profile
    mlcanopy_inst__shsoi_soil = mlcanopy_inst.shsoi_soil
    mlcanopy_inst__shsrc_profile = mlcanopy_inst.shsrc_profile
    mlcanopy_inst__shveg_canopy = mlcanopy_inst.shveg_canopy
    mlcanopy_inst__shvegsha_canopy = mlcanopy_inst.shvegsha_canopy
    mlcanopy_inst__shvegsun_canopy = mlcanopy_inst.shvegsun_canopy
    mlcanopy_inst__soil_dz_soil = mlcanopy_inst.soil_dz_soil
    mlcanopy_inst__soil_et_loss_soil = mlcanopy_inst.soil_et_loss_soil
    mlcanopy_inst__soil_t_soil = mlcanopy_inst.soil_t_soil
    mlcanopy_inst__soil_tk_soil = mlcanopy_inst.soil_tk_soil
    mlcanopy_inst__soilres_soil = mlcanopy_inst.soilres_soil
    mlcanopy_inst__solar_zen_forcing = mlcanopy_inst.solar_zen_forcing
    mlcanopy_inst__stair_profile = mlcanopy_inst.stair_profile
    mlcanopy_inst__stflx_air_canopy = mlcanopy_inst.stflx_air_canopy
    mlcanopy_inst__stflx_veg_canopy = mlcanopy_inst.stflx_veg_canopy
    mlcanopy_inst__stleaf_leaf = mlcanopy_inst.stleaf_leaf
    mlcanopy_inst__stleaf_mean_profile = mlcanopy_inst.stleaf_mean_profile
    mlcanopy_inst__stsrc_profile = mlcanopy_inst.stsrc_profile
    mlcanopy_inst__swbeam_profile = mlcanopy_inst.swbeam_profile
    mlcanopy_inst__swdwn_profile = mlcanopy_inst.swdwn_profile
    mlcanopy_inst__swleaf_leaf = mlcanopy_inst.swleaf_leaf
    mlcanopy_inst__swleaf_mean_profile = mlcanopy_inst.swleaf_mean_profile
    mlcanopy_inst__swskyb_bef_forcing = mlcanopy_inst.swskyb_bef_forcing
    mlcanopy_inst__swskyb_cur_forcing = mlcanopy_inst.swskyb_cur_forcing
    mlcanopy_inst__swskyb_forcing = mlcanopy_inst.swskyb_forcing
    mlcanopy_inst__swskyd_bef_forcing = mlcanopy_inst.swskyd_bef_forcing
    mlcanopy_inst__swskyd_cur_forcing = mlcanopy_inst.swskyd_cur_forcing
    mlcanopy_inst__swskyd_forcing = mlcanopy_inst.swskyd_forcing
    mlcanopy_inst__swsoi_soil = mlcanopy_inst.swsoi_soil
    mlcanopy_inst__swsrc_profile = mlcanopy_inst.swsrc_profile
    mlcanopy_inst__swupw_profile = mlcanopy_inst.swupw_profile
    mlcanopy_inst__swveg_canopy = mlcanopy_inst.swveg_canopy
    mlcanopy_inst__swvegsha_canopy = mlcanopy_inst.swvegsha_canopy
    mlcanopy_inst__swvegsun_canopy = mlcanopy_inst.swvegsun_canopy
    mlcanopy_inst__tacclim_forcing = mlcanopy_inst.tacclim_forcing
    mlcanopy_inst__taf_canopy = mlcanopy_inst.taf_canopy
    mlcanopy_inst__tair_bef_profile = mlcanopy_inst.tair_bef_profile
    mlcanopy_inst__tair_profile = mlcanopy_inst.tair_profile
    mlcanopy_inst__taveg_canopy = mlcanopy_inst.taveg_canopy
    mlcanopy_inst__tavegsha_canopy = mlcanopy_inst.tavegsha_canopy
    mlcanopy_inst__tavegsun_canopy = mlcanopy_inst.tavegsun_canopy
    mlcanopy_inst__tb_profile = mlcanopy_inst.tb_profile
    mlcanopy_inst__tbi_profile = mlcanopy_inst.tbi_profile
    mlcanopy_inst__td_profile = mlcanopy_inst.td_profile
    mlcanopy_inst__tg_bef_soil = mlcanopy_inst.tg_bef_soil
    mlcanopy_inst__tg_soil = mlcanopy_inst.tg_soil
    mlcanopy_inst__thref_forcing = mlcanopy_inst.thref_forcing
    mlcanopy_inst__thvref_forcing = mlcanopy_inst.thvref_forcing
    mlcanopy_inst__tleaf_bef_leaf = mlcanopy_inst.tleaf_bef_leaf
    mlcanopy_inst__tleaf_hist_leaf = mlcanopy_inst.tleaf_hist_leaf
    mlcanopy_inst__tleaf_leaf = mlcanopy_inst.tleaf_leaf
    mlcanopy_inst__tleaf_mean_profile = mlcanopy_inst.tleaf_mean_profile
    mlcanopy_inst__tlveg_canopy = mlcanopy_inst.tlveg_canopy
    mlcanopy_inst__tlvegsha_canopy = mlcanopy_inst.tlvegsha_canopy
    mlcanopy_inst__tlvegsun_canopy = mlcanopy_inst.tlvegsun_canopy
    mlcanopy_inst__tref_bef_forcing = mlcanopy_inst.tref_bef_forcing
    mlcanopy_inst__tref_cur_forcing = mlcanopy_inst.tref_cur_forcing
    mlcanopy_inst__tref_forcing = mlcanopy_inst.tref_forcing
    mlcanopy_inst__trleaf_leaf = mlcanopy_inst.trleaf_leaf
    mlcanopy_inst__trleaf_mean_profile = mlcanopy_inst.trleaf_mean_profile
    mlcanopy_inst__trsrc_profile = mlcanopy_inst.trsrc_profile
    mlcanopy_inst__trveg_canopy = mlcanopy_inst.trveg_canopy
    mlcanopy_inst__uaf_canopy = mlcanopy_inst.uaf_canopy
    mlcanopy_inst__uref_bef_forcing = mlcanopy_inst.uref_bef_forcing
    mlcanopy_inst__uref_cur_forcing = mlcanopy_inst.uref_cur_forcing
    mlcanopy_inst__uref_forcing = mlcanopy_inst.uref_forcing
    mlcanopy_inst__ustar_canopy = mlcanopy_inst.ustar_canopy
    mlcanopy_inst__vcmax25_leaf = mlcanopy_inst.vcmax25_leaf
    mlcanopy_inst__vcmax25_profile = mlcanopy_inst.vcmax25_profile
    mlcanopy_inst__vcmax25sha_canopy = mlcanopy_inst.vcmax25sha_canopy
    mlcanopy_inst__vcmax25sun_canopy = mlcanopy_inst.vcmax25sun_canopy
    mlcanopy_inst__vcmax25veg_canopy = mlcanopy_inst.vcmax25veg_canopy
    mlcanopy_inst__vcmax_leaf = mlcanopy_inst.vcmax_leaf
    mlcanopy_inst__vpd_leaf = mlcanopy_inst.vpd_leaf
    mlcanopy_inst__wind_profile = mlcanopy_inst.wind_profile
    mlcanopy_inst__windveg_canopy = mlcanopy_inst.windveg_canopy
    mlcanopy_inst__windvegsha_canopy = mlcanopy_inst.windvegsha_canopy
    mlcanopy_inst__windvegsun_canopy = mlcanopy_inst.windvegsun_canopy
    mlcanopy_inst__z0m_canopy = mlcanopy_inst.z0m_canopy
    mlcanopy_inst__zbot_canopy = mlcanopy_inst.zbot_canopy
    mlcanopy_inst__zdisp_canopy = mlcanopy_inst.zdisp_canopy
    mlcanopy_inst__zref_forcing = mlcanopy_inst.zref_forcing
    mlcanopy_inst__zs_profile = mlcanopy_inst.zs_profile
    mlcanopy_inst__ztop_canopy = mlcanopy_inst.ztop_canopy
    mlcanopy_inst__zw_profile = mlcanopy_inst.zw_profile
    solarabs_inst__fsa_patch = solarabs_inst.fsa_patch
    surfalb_inst__albd_patch = surfalb_inst.albd_patch
    surfalb_inst__albi_patch = surfalb_inst.albi_patch
    temperature_inst__t_ref2m_patch = temperature_inst.t_ref2m_patch
    waterdiagnosticbulk_inst__q_ref2m_patch = waterdiagnosticbulk_inst.q_ref2m_patch
    waterfluxbulk_inst__qflx_evap_tot_patch = waterfluxbulk_inst.qflx_evap_tot_patch
    clm_time_manager__curr_date_ymd = _clm_time_manager.curr_date_ymd
    mlclm_varcon__jmax25_to_vcmax25_acclim = _mlclm_varcon.jmax25_to_vcmax25_acclim
    mlclm_varcon__jmaxse_acclim = _mlclm_varcon.jmaxse_acclim
    mlclm_varcon__vcmaxse_acclim = _mlclm_varcon.vcmaxse_acclim
    mlclm_varctl__ml_vert_init = _mlclm_varctl.ml_vert_init
    return energyflux_inst__eflx_lh_tot_patch, energyflux_inst__eflx_lwrad_out_patch, energyflux_inst__eflx_sh_tot_patch, energyflux_inst__taux_patch, energyflux_inst__tauy_patch, frictionvel_inst__fv_patch, frictionvel_inst__u10_clm_patch, mlcanopy_inst__ac_leaf, mlcanopy_inst__agross_leaf, mlcanopy_inst__aj_leaf, mlcanopy_inst__albcan_canopy, mlcanopy_inst__albsoib_soil, mlcanopy_inst__albsoid_soil, mlcanopy_inst__anet_leaf, mlcanopy_inst__ap_leaf, mlcanopy_inst__apar_leaf, mlcanopy_inst__apar_mean_profile, mlcanopy_inst__beta_canopy, mlcanopy_inst__btran_soil, mlcanopy_inst__cair_bef_profile, mlcanopy_inst__cair_profile, mlcanopy_inst__ceair_leaf, mlcanopy_inst__ci_leaf, mlcanopy_inst__co2ref_bef_forcing, mlcanopy_inst__co2ref_cur_forcing, mlcanopy_inst__co2ref_forcing, mlcanopy_inst__cp_leaf, mlcanopy_inst__cpair_forcing, mlcanopy_inst__cpleaf_profile, mlcanopy_inst__cs_leaf, mlcanopy_inst__deair_profile, mlcanopy_inst__dh2ocan_profile, mlcanopy_inst__dlai_frac_profile, mlcanopy_inst__dlai_profile, mlcanopy_inst__dlwp_leaf, mlcanopy_inst__dpai_profile, mlcanopy_inst__dsai_frac_profile, mlcanopy_inst__dsai_profile, mlcanopy_inst__dtair_profile, mlcanopy_inst__dtg_soil, mlcanopy_inst__dtleaf_leaf, mlcanopy_inst__dz_profile, mlcanopy_inst__eair_bef_profile, mlcanopy_inst__eair_profile, mlcanopy_inst__eg_soil, mlcanopy_inst__eref_forcing, mlcanopy_inst__etair_profile, mlcanopy_inst__etflx_canopy, mlcanopy_inst__etleaf_mean_profile, mlcanopy_inst__etsoi_soil, mlcanopy_inst__etsrc_profile, mlcanopy_inst__etveg_canopy, mlcanopy_inst__etvegsha_canopy, mlcanopy_inst__etvegsun_canopy, mlcanopy_inst__evleaf_leaf, mlcanopy_inst__evleaf_mean_profile, mlcanopy_inst__evsrc_profile, mlcanopy_inst__evveg_canopy, mlcanopy_inst__fco2_mean_profile, mlcanopy_inst__fco2src_profile, mlcanopy_inst__fdry_profile, mlcanopy_inst__fracminlwp_canopy, mlcanopy_inst__fracsun_profile, mlcanopy_inst__fwet_profile, mlcanopy_inst__g0_canopy, mlcanopy_inst__g1_canopy, mlcanopy_inst__gac0_soil, mlcanopy_inst__gac_profile, mlcanopy_inst__gac_to_hc_canopy, mlcanopy_inst__gbc_leaf, mlcanopy_inst__gbh_leaf, mlcanopy_inst__gbv_leaf, mlcanopy_inst__gppveg_canopy, mlcanopy_inst__gppvegsha_canopy, mlcanopy_inst__gppvegsun_canopy, mlcanopy_inst__gs_leaf, mlcanopy_inst__gs_mean_profile, mlcanopy_inst__gsoi_soil, mlcanopy_inst__gspot_leaf, mlcanopy_inst__gsveg_canopy, mlcanopy_inst__gsvegsha_canopy, mlcanopy_inst__gsvegsun_canopy, mlcanopy_inst__h2ocan_bef_profile, mlcanopy_inst__h2ocan_profile, mlcanopy_inst__hs_leaf, mlcanopy_inst__je_leaf, mlcanopy_inst__jmax25_leaf, mlcanopy_inst__jmax25_profile, mlcanopy_inst__jmax_leaf, mlcanopy_inst__kb_profile, mlcanopy_inst__kc_eddy_profile, mlcanopy_inst__kc_leaf, mlcanopy_inst__ko_leaf, mlcanopy_inst__kp25_leaf, mlcanopy_inst__kp25_profile, mlcanopy_inst__kp_leaf, mlcanopy_inst__lai_canopy, mlcanopy_inst__laisha_canopy, mlcanopy_inst__laisun_canopy, mlcanopy_inst__lc_canopy, mlcanopy_inst__leaf_esat_leaf, mlcanopy_inst__lhflx_canopy, mlcanopy_inst__lhleaf_leaf, mlcanopy_inst__lhleaf_mean_profile, mlcanopy_inst__lhsoi_soil, mlcanopy_inst__lhsrc_profile, mlcanopy_inst__lhveg_canopy, mlcanopy_inst__lhvegsha_canopy, mlcanopy_inst__lhvegsun_canopy, mlcanopy_inst__lsc_profile, mlcanopy_inst__lwdwn_profile, mlcanopy_inst__lwleaf_leaf, mlcanopy_inst__lwleaf_mean_profile, mlcanopy_inst__lwp_bef_leaf, mlcanopy_inst__lwp_hist_leaf, mlcanopy_inst__lwp_leaf, mlcanopy_inst__lwp_mean_profile, mlcanopy_inst__lwsky_bef_forcing, mlcanopy_inst__lwsky_cur_forcing, mlcanopy_inst__lwsky_forcing, mlcanopy_inst__lwsoi_soil, mlcanopy_inst__lwsrc_profile, mlcanopy_inst__lwup_canopy, mlcanopy_inst__lwupw_profile, mlcanopy_inst__lwveg_canopy, mlcanopy_inst__lwvegsha_canopy, mlcanopy_inst__lwvegsun_canopy, mlcanopy_inst__mflx_profile, mlcanopy_inst__mmair_forcing, mlcanopy_inst__nbot_canopy, mlcanopy_inst__ncan_canopy, mlcanopy_inst__ntop_canopy, mlcanopy_inst__o2ref_forcing, mlcanopy_inst__obu_canopy, mlcanopy_inst__pbeta_lai_canopy, mlcanopy_inst__pbeta_sai_canopy, mlcanopy_inst__pref_bef_forcing, mlcanopy_inst__pref_cur_forcing, mlcanopy_inst__pref_forcing, mlcanopy_inst__prsc_canopy, mlcanopy_inst__psis_soil, mlcanopy_inst__qaf_canopy, mlcanopy_inst__qflx_intr_canopy, mlcanopy_inst__qflx_rain_forcing, mlcanopy_inst__qflx_snow_forcing, mlcanopy_inst__qflx_tflrain_canopy, mlcanopy_inst__qflx_tflsnow_canopy, mlcanopy_inst__qref_bef_forcing, mlcanopy_inst__qref_cur_forcing, mlcanopy_inst__qref_forcing, mlcanopy_inst__rd25_leaf, mlcanopy_inst__rd25_profile, mlcanopy_inst__rd_leaf, mlcanopy_inst__rhg_soil, mlcanopy_inst__rhoair_forcing, mlcanopy_inst__rhomol_forcing, mlcanopy_inst__rnet_canopy, mlcanopy_inst__rnleaf_leaf, mlcanopy_inst__rnleaf_mean_profile, mlcanopy_inst__rnsoi_soil, mlcanopy_inst__rnsrc_profile, mlcanopy_inst__rsoil_soil, mlcanopy_inst__sai_canopy, mlcanopy_inst__shair_profile, mlcanopy_inst__shflx_canopy, mlcanopy_inst__shleaf_leaf, mlcanopy_inst__shleaf_mean_profile, mlcanopy_inst__shsoi_soil, mlcanopy_inst__shsrc_profile, mlcanopy_inst__shveg_canopy, mlcanopy_inst__shvegsha_canopy, mlcanopy_inst__shvegsun_canopy, mlcanopy_inst__soil_dz_soil, mlcanopy_inst__soil_et_loss_soil, mlcanopy_inst__soil_t_soil, mlcanopy_inst__soil_tk_soil, mlcanopy_inst__soilres_soil, mlcanopy_inst__solar_zen_forcing, mlcanopy_inst__stair_profile, mlcanopy_inst__stflx_air_canopy, mlcanopy_inst__stflx_veg_canopy, mlcanopy_inst__stleaf_leaf, mlcanopy_inst__stleaf_mean_profile, mlcanopy_inst__stsrc_profile, mlcanopy_inst__swbeam_profile, mlcanopy_inst__swdwn_profile, mlcanopy_inst__swleaf_leaf, mlcanopy_inst__swleaf_mean_profile, mlcanopy_inst__swskyb_bef_forcing, mlcanopy_inst__swskyb_cur_forcing, mlcanopy_inst__swskyb_forcing, mlcanopy_inst__swskyd_bef_forcing, mlcanopy_inst__swskyd_cur_forcing, mlcanopy_inst__swskyd_forcing, mlcanopy_inst__swsoi_soil, mlcanopy_inst__swsrc_profile, mlcanopy_inst__swupw_profile, mlcanopy_inst__swveg_canopy, mlcanopy_inst__swvegsha_canopy, mlcanopy_inst__swvegsun_canopy, mlcanopy_inst__tacclim_forcing, mlcanopy_inst__taf_canopy, mlcanopy_inst__tair_bef_profile, mlcanopy_inst__tair_profile, mlcanopy_inst__taveg_canopy, mlcanopy_inst__tavegsha_canopy, mlcanopy_inst__tavegsun_canopy, mlcanopy_inst__tb_profile, mlcanopy_inst__tbi_profile, mlcanopy_inst__td_profile, mlcanopy_inst__tg_bef_soil, mlcanopy_inst__tg_soil, mlcanopy_inst__thref_forcing, mlcanopy_inst__thvref_forcing, mlcanopy_inst__tleaf_bef_leaf, mlcanopy_inst__tleaf_hist_leaf, mlcanopy_inst__tleaf_leaf, mlcanopy_inst__tleaf_mean_profile, mlcanopy_inst__tlveg_canopy, mlcanopy_inst__tlvegsha_canopy, mlcanopy_inst__tlvegsun_canopy, mlcanopy_inst__tref_bef_forcing, mlcanopy_inst__tref_cur_forcing, mlcanopy_inst__tref_forcing, mlcanopy_inst__trleaf_leaf, mlcanopy_inst__trleaf_mean_profile, mlcanopy_inst__trsrc_profile, mlcanopy_inst__trveg_canopy, mlcanopy_inst__uaf_canopy, mlcanopy_inst__uref_bef_forcing, mlcanopy_inst__uref_cur_forcing, mlcanopy_inst__uref_forcing, mlcanopy_inst__ustar_canopy, mlcanopy_inst__vcmax25_leaf, mlcanopy_inst__vcmax25_profile, mlcanopy_inst__vcmax25sha_canopy, mlcanopy_inst__vcmax25sun_canopy, mlcanopy_inst__vcmax25veg_canopy, mlcanopy_inst__vcmax_leaf, mlcanopy_inst__vpd_leaf, mlcanopy_inst__wind_profile, mlcanopy_inst__windveg_canopy, mlcanopy_inst__windvegsha_canopy, mlcanopy_inst__windvegsun_canopy, mlcanopy_inst__z0m_canopy, mlcanopy_inst__zbot_canopy, mlcanopy_inst__zdisp_canopy, mlcanopy_inst__zref_forcing, mlcanopy_inst__zs_profile, mlcanopy_inst__ztop_canopy, mlcanopy_inst__zw_profile, solarabs_inst__fsa_patch, surfalb_inst__albd_patch, surfalb_inst__albi_patch, temperature_inst__t_ref2m_patch, waterdiagnosticbulk_inst__q_ref2m_patch, waterfluxbulk_inst__qflx_evap_tot_patch, clm_time_manager__curr_date_ymd, mlclm_varcon__jmax25_to_vcmax25_acclim, mlclm_varcon__jmaxse_acclim, mlclm_varcon__vcmaxse_acclim, mlclm_varctl__ml_vert_init

_SIGNATURES.update({
    'mlcanopyfluxes_flat': {'kind': 'subroutine', 'args': [{'name': 'num_exposedvegp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'filter_exposedvegp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'np_', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'atm2lnd_inst__forc_lwrad_downscaled_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'atm2lnd_inst__forc_pbot_downscaled_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'atm2lnd_inst__forc_pco2_grc', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'atm2lnd_inst__forc_po2_grc', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'atm2lnd_inst__forc_solad_downscaled_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'atm2lnd_inst__forc_solai_grc', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'atm2lnd_inst__forc_t_downscaled_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'atm2lnd_inst__forc_u_grc', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'atm2lnd_inst__forc_v_grc', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'bounds__begp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}, {'name': 'bounds__endp', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': []}, {'name': 'canopystate_inst__elai_patch', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'canopystate_inst__esai_patch', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'canopystate_inst__htop_patch', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'col__dz', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - ((-clm_varpar__nlevsno+1)) + 1'}]}, {'name': 'col__nbedrock', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'col__snl', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'col__z', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - ((-clm_varpar__nlevsno+1)) + 1'}]}, {'name': 'col__zi', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - ((-clm_varpar__nlevsno+0)) + 1'}]}, {'name': 'energyflux_inst__eflx_lh_tot_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'energyflux_inst__eflx_lwrad_out_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'energyflux_inst__eflx_sh_tot_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'energyflux_inst__taux_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'energyflux_inst__tauy_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'frictionvel_inst__forc_hgt_u_patch', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'frictionvel_inst__fv_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'frictionvel_inst__u10_clm_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'grc__latdeg', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'grc__londeg', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ac_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__agross_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__aj_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__albcan_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__albsoib_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__albsoid_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__anet_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ap_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__apar_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__apar_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__beta_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__btran_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__cair_bef_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__cair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__ceair_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ci_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__co2ref_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__co2ref_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__co2ref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__co2ref_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__cp_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__cpair_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__cpleaf_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__cs_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__deair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '4'}]}, {'name': 'mlcanopy_inst__dh2ocan_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '4'}]}, {'name': 'mlcanopy_inst__dlai_frac_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__dlai_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__dlwp_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}, {'lb': '1', 'ub': '4'}]}, {'name': 'mlcanopy_inst__dpai_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__dsai_frac_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__dsai_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__dtair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '4'}]}, {'name': 'mlcanopy_inst__dtg_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '4'}]}, {'name': 'mlcanopy_inst__dtleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}, {'lb': '1', 'ub': '4'}]}, {'name': 'mlcanopy_inst__dz_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__eair_bef_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__eair_data_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__eair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__eg_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__eref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__etair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__etflx_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__etleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__etsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__etsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__etveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__etvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__etvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__evleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__evleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__evsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__evveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__fco2_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__fco2src_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__fdry_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__fracminlwp_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__fracsun_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__fwet_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__g0_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__g1_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gac0_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gac_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__gac_to_hc_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gbc_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gbh_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gbv_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gppveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gppvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gppvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gs_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gs_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__gsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gspot_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__gsveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gsvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__gsvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__h2ocan_bef_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__h2ocan_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__hs_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__je_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__jmax25_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__jmax25_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__jmax_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__kb_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__kc_eddy_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__kc_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__ko_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__kp25_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__kp25_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__kp_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lai_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__laisha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__laisun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lc_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__leaf_esat_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lhflx_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lhleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lhleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lhsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lhsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lhveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lhvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lhvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lsc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lwdwn_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}]}, {'name': 'mlcanopy_inst__lwleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lwleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lwp_bef_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lwp_hist_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lwp_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__lwp_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lwsky_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwsky_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwsky_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwsky_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__lwup_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwupw_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}]}, {'name': 'mlcanopy_inst__lwveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__lwvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__mflx_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__mmair_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__nbot_canopy', 'dtype': 'int32', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ncan_canopy', 'dtype': 'int32', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ntop_canopy', 'dtype': 'int32', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__o2ref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__obu_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__pbeta_lai_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__pbeta_sai_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__pref_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__pref_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__pref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__pref_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__prsc_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__psis_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qaf_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qflx_intr_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qflx_rain_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qflx_snow_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qflx_tflrain_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qflx_tflsnow_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qref_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qref_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__qref_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rd25_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__rd25_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__rd_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__rhg_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rhoair_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rhomol_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rnet_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rnleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__rnleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__rnsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rnsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__root_biomass_canopy', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__rsoil_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__sai_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__shair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__shflx_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__shleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__shleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__shsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__shsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__shveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__shvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__shvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__soil_dz_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__soil_et_loss_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - (1) + 1'}]}, {'name': 'mlcanopy_inst__soil_t_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__soil_tk_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__soilres_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__solar_zen_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__stair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__stflx_air_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__stflx_veg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__stleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__stleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__stsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__swbeam_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swdwn_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyb_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyb_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyb_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyb_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyd_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyd_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyd_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swskyd_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swsoi_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swupw_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__swvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__tacclim_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__taf_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tair_bef_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__tair_data_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__tair_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__taveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tavegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tavegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tb_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__tbi_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}]}, {'name': 'mlcanopy_inst__td_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__tg_bef_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tg_soil', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__thref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__thvref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tleaf_bef_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__tleaf_hist_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__tleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__tleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__tlveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tlvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tlvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tref_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tref_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__tref_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__trleaf_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__trleaf_mean_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__trsrc_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__trveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__uaf_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__uref_bef_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__uref_cur_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__uref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__uref_next_forcing', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__ustar_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__vcmax25_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__vcmax25_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__vcmax25sha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__vcmax25sun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__vcmax25veg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__vcmax_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__vpd_leaf', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}, {'lb': '1', 'ub': '2'}]}, {'name': 'mlcanopy_inst__wind_data_profile', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__wind_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__windveg_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__windvegsha_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__windvegsun_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__z0m_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zbot_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zdisp_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zref_forcing', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zs_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '100'}]}, {'name': 'mlcanopy_inst__ztop_canopy', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'mlcanopy_inst__zw_profile', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '101'}]}, {'name': 'mlpftcon__capac_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__clump_fac', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__emleaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__g0_bb', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__g0_med', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__g1_bb', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__g1_med', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__gplant_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__gsmin_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__iota_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__psi50_gs', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__root_density_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__root_radius_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__root_resist_spa', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__shape_gs', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'mlpftcon__vcmaxpft', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'patch__column', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'patch__gridcell', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'patch__itype', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'pftcon__c3psn', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'pftcon__dleaf', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'pftcon__rhol', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__rhos', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__slatop', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'pftcon__taul', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__taus', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}, {'lb': '1', 'ub': '2'}]}, {'name': 'pftcon__xl', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '79'}]}, {'name': 'soilstate_inst__hk_l_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - (1) + 1'}]}, {'name': 'soilstate_inst__rootfr_patch', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - (1) + 1'}]}, {'name': 'soilstate_inst__smp_l_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - (1) + 1'}]}, {'name': 'soilstate_inst__soilresis_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'soilstate_inst__thk_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - ((-clm_varpar__nlevsno+1)) + 1'}]}, {'name': 'solarabs_inst__fsa_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'surfalb_inst__albd_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'surfalb_inst__albgrd_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'surfalb_inst__albgri_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'surfalb_inst__albi_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '2'}]}, {'name': 'temperature_inst__t_a10_patch', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'temperature_inst__t_ref2m_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'temperature_inst__t_soisno_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - ((-clm_varpar__nlevsno+1)) + 1'}]}, {'name': 'wateratm2lndbulk_inst__forc_q_downscaled_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'wateratm2lndbulk_inst__forc_rain_downscaled_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'wateratm2lndbulk_inst__forc_snow_downscaled_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'waterdiagnosticbulk_inst__q_ref2m_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'waterfluxbulk_inst__qflx_evap_tot_patch', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}]}, {'name': 'waterstatebulk_inst__h2osoi_ice_col', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': 'np_'}, {'lb': '1', 'ub': '((clm_varpar__nlevgrnd)) - ((-clm_varpar__nlevsno+1)) + 1'}]}, {'name': 'clm_time_manager__curr_date_ymd', 'dtype': 'int32', 'intent': 'INOUT', 'optional': False, 'dims': None}, {'name': 'clm_time_manager__dtstep', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_time_manager__itim', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_time_manager__start_date_tod', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_time_manager__start_date_ymd', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__cpliq', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__denh2o', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__grav', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__hsub', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__hvap', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__sb', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varcon__vkc', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varorb__eccen', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varorb__lambm0', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varorb__mvelpp', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varorb__obliqr', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varpar__nlevgrnd', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varpar__nlevsno', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'clm_varpar__nlevsoi', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__ah12', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '3'}]}, {'name': 'mlclm_varcon__beta_neutral_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__c2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cd', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__chil_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__chil_min', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__colim_c3a', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__colim_c4a', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__colim_c4b', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cp25', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cpbio', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cpd', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cpha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cpw', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__cr', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__dc0', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__dewmx', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__dh0', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__dh2o_to_dco2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__dtlgridh', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '1'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__dtlgridm', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '1'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__dv0', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__emg', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__eta_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__fcarbon', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__fwater', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__fwet_exponent', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__gb_factor', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__gbh_min', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__interception_fraction', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__j_to_umol', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmax25_to_vcmax25_acclim', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmax25_to_vcmax25_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxha_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxha_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxhd_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxhd_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxse_acclim', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__jmaxse_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__kb_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__kc25', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__kcha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__ko25', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__koha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__kp25_to_vcmax25_c4', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__lapse_rate', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__lcl_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__lcl_min', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__maximum_leaf_wetted_fraction', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__mmdry', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__mmh2o', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__phi_psii', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__pr0', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__pr1', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__pr2', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__psigridh', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__psigridm', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '41'}]}, {'name': 'mlclm_varcon__qe_c4', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__ra_max', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rd25_to_vcmax25_c3', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rd25_to_vcmax25_c4', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rdha', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rdhd', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rdse', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rgas', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__rh_min_bb', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__theta_j', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxha_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxha_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxhd_acclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxhd_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxse_acclim', 'dtype': 'float64', 'intent': 'INOUT', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vcmaxse_noacclim', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__visc0', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__vpd_min_med', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__wind_forc_min', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__z0mg', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varcon__zdtgridh', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '1'}]}, {'name': 'mlclm_varcon__zdtgridm', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': [{'lb': '1', 'ub': '276'}, {'lb': '1', 'ub': '1'}]}, {'name': 'mlclm_varctl__acclim_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__colim_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__dpai_min', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__dtime_ml', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__dz_param', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__dz_short', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__dz_tall', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__flux_profile_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__gb_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__gs_solver', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__gs_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__gspot_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__hf_extension_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__kn_val', 'dtype': 'float64', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__leaf_optics_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__light_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__longwave_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__met_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__ml_vert_init', 'dtype': 'int32', 'intent': 'INOUT', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__mlcan_to_clm', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__nlayer_above', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__nlayer_within', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__sparse_canopy_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}, {'name': 'mlclm_varctl__turb_type', 'dtype': 'int32', 'intent': 'IN', 'optional': False, 'dims': None}], 'result': None, 'result_dtype': None},
})
