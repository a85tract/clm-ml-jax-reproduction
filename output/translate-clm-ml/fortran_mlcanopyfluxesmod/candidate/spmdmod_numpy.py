"""Stand-in for Fortran module spmdmod, written by RecastEngine.

Not a translation: the module is a stub under the frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

masterproc = True
iam = 0
npes = 1

