# ./lib/func.py

"""
Not yet implemented.
"""

__all__ = ()

WRAPPED_STATIC_FUNCTION = "__wrappedstaticfunction__"


def _func_name(func):
    return func.__name__

def _func_varnames(func):
    return func.__code__.co_varnames

def _func_annotations(func):
    return func.__annotations__

def _func_base(func):
    return getattr(func, WRAPPED_STATIC_FUNCTION, func)

def _func_base_varnames(func):
    return _func_varnames(
        _func_base(func)
        )
