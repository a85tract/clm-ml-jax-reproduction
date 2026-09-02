"""Stand-in for Fortran module clm_varpar, written by recast-clm.

Not a translation: the module is a stub under the clm frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

NLEVSNO = (-1)  # clm_varpar.f90:16
NLEVSOI = (-1)  # clm_varpar.f90:17
NLEVGRND = (-1)  # clm_varpar.f90:18
NUMRAD = 2  # clm_varpar.f90:20
IVIS = 1  # clm_varpar.f90:21
INIR = 2  # clm_varpar.f90:22
MXPFT = 78  # clm_varpar.f90:23

nlevsno = NLEVSNO
nlevsoi = NLEVSOI
nlevgrnd = NLEVGRND
numrad = NUMRAD
ivis = IVIS
inir = INIR
mxpft = MXPFT

