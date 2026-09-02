"""Stand-in for Fortran module shr_kind_mod, written by recast-clm.

Not a translation: the module is a stub under the clm frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

shr_kind_r8 = np.float64
shr_kind_r4 = np.float32
shr_kind_i8 = np.int64
shr_kind_i4 = np.int32
shr_kind_cs = 80
shr_kind_cl = 256
shr_kind_cx = 512

