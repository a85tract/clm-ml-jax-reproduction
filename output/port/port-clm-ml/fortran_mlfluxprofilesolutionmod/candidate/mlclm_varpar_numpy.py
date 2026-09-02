"""Stand-in for Fortran module mlclm_varpar, written by RecastEngine.

Not a translation: the module is a stub under the frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

NLEVMLCAN = 100  # MLclm_varpar.f90:18
NLEAF = 2  # MLclm_varpar.f90:19
ISUN = 1  # MLclm_varpar.f90:20
ISHA = 2  # MLclm_varpar.f90:21

nlevmlcan = NLEVMLCAN
nleaf = NLEAF
isun = ISUN
isha = ISHA

