# ./lib/decorate.py

"""
Not yet implemented.
"""

from .param import _set_accepts, _accepts_from_declared, \
                    _accepts_from_annotations, _set_returns, \
                    _returns_from_annotations


__all__ = (
    "accepts",
    "returns",
    "statictyped",
    )


def statictyped(func):
    """"""
    accepts = _accepts_from_annotations(func)
    returns = _returns_from_annotations(func)
    func = _set_accepts(func, accepts)
    func = _set_returns(func, returns)
    return func

def accepts(*dtypes, **kwdtypes):
    """"""
    def _acceptswrapper(func):
        _dtypes = _accepts_from_declared(func, dtypes, kwdtypes)
        return _set_accepts(func, _dtypes)
    return _acceptswrapper

def returns(dtype):
    """"""
    def _returnswrapper(func):
        return _set_returns(func, dtype)
    return _returnswrapper
