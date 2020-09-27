# ./lib/type.py

"""
Not yet implemented.
"""

from collections.abc import Sequence

from .func import _func_name, _func_varnames, _func_base_varnames

from .exception import StaticTypeError


__all__ = (
    "NUMERIC",
    )

ACCEPTABLE_TYPES = (None, ())
NUMERIC = (int, float)


def _typecheck_accepts(func, accepts, args, kwargs):
    funcname, varnames = _func_name(func), _func_base_varnames(func)
    inputs = {
        **{varnames[i]: v for i, v in enumerate(args)},
        **kwargs
        }
    for k, v in inputs.items():
        dtype = accepts[k]
        if not _typecheck_arg(v, dtype):
            raise StaticTypeError(
                f"Parameter '{k}' of '{funcname}' " \
                f"only accepts {dtype}; Invalid type {type(v)} was provided."
                )
    return func

def _typecheck_returns(func, returns, value):
    funcname = _func_name(func)
    if not _typecheck_arg(value, returns):
        if isinstance(returns, Sequence) and len(returns) < 2:
            returns = returns[0]
        raise StaticTypeError(
            f"'{funcname}' must return '{str(returns)}'; " \
            f"Invalid type '{type(value)}' returned."
            )
    return func

def _typecheck_arg(arg, dtype):
    return dtype in ACCEPTABLE_TYPES or isinstance(arg, dtype)

def _typecast_accepts(args, accepts):
    pass

def _typecast_returns(arg, returns):
    pass

def _typecast_arg(arg, dtype):
    pass
