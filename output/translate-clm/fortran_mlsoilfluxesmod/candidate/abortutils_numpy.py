"""Stand-in for Fortran module abortutils, written by recast-clm.

Not a translation: the module is a stub under the clm frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

def endrun(msg='', *_args, **_kwargs):
    raise RuntimeError(f'endrun: {msg}')

def handle_err(status, errmsg='', *_args, **_kwargs):
    raise RuntimeError(f'handle_err {status}: {errmsg}')

