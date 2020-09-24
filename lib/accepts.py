# ./lib/accepts.py

"""
Not yet implemented.
"""

from collections.abc import Iterable, Sequence
from functools import wraps


__all__ = ()

RETURN = "return"


class StaticTypeError(TypeError):
    pass


def statictyped(func):
    varnames = _func_varnames(func)
    accepts = _accepts_from_annotations(varnames, func.__annotations__)
    returns = _returns_from_annotations(func.__annotations__)
    return StaticTypedMethod(func, accepts, returns)

def accepts(**dtypes):
    def _accepts_setter(func):
        method = _create_statictyped_method(func)
        _dtypes = _accepts_from_annotations(
            _func_varnames(func),
            dtypes
            )
        _set_accepts(method, _dtypes)
        return method
    return _accepts_setter

def returns(dtype):
    def _returns_setter(func):
        method = _create_statictyped_method(func)
        _set_returns(method, dtype)
        return method
    return _returns_setter

def _create_statictyped_method(func):
    if isinstance(func, StaticTypedMethod):
        return func
    else:
        return StaticTypedMethod(func)

def _func_varnames(func):
    if not isinstance(func, StaticTypedMethod):
        return func.__code__.co_varnames
    else:
        return func.varnames

def _to_empty_iterable(value, type=tuple):
    if value is None:
        value = type()
    return _to_iterable(value, type)

def _to_iterable(value, type=tuple):
    if isinstance(value, str) or not isinstance(value, Iterable):
        value = (i for i in (value,))

    if type is not None and not isinstance(value, type):
        if issubclass(type, dict):
            value = enumerate(value)
        value = type(value)

    return value

def _accepts_from_annotations(varnames, annotations):
    return tuple(
        annotations.get(i, None) for i in varnames
        )

def _returns_from_annotations(annotations):
    return (annotations.get(RETURN),)

def _typecheck_arg(arg, dtype):
    return dtype is None or dtype == () or isinstance(arg, dtype)

def _typecheck_inputs(funcname, varnames, accepts, args, kwargs):
    inputs = (*args, *kwargs.values())
    for i, v in enumerate(inputs):
        dtype = accepts[i]
        if not _typecheck_arg(v, dtype):
            raise StaticTypeError(
                f"Parameter '{varnames[i]}' of '{funcname}' " \
                f"only accepts {dtype}; Invalid type {type(v)} was provided."
                )

def _typecheck_output(funcname, returns, value):
    if not _typecheck_arg(value, returns):
        if isinstance(returns, Sequence) and len(returns) < 2:
            returns = returns[0]
        raise StaticTypeError(
            f"'{funcname}' must return '{str(returns)}'; " \
            f"Invalid type '{type(value)}' returned."
            )

def _set_accepts(self, accepts):
    self._accepts = _to_empty_iterable(accepts)

def _set_returns(self, returns):
    self._returns = _to_empty_iterable(returns)

def _wrap_func(self, func):
    wraps(func)(self)


class StaticTypedMethod:
    def __init__(self, func, accepts=None, returns=None):
        self._func = func
        _set_accepts(self, accepts)
        _set_returns(self, accepts)
        _wrap_func(self, func)

    @property
    def accepts(self):
        self._accepts

    @property
    def returns(self):
        self._returns

    @property
    def varnames(self):
        varnames = _func_varnames(self._func)
        return {varnames[i]: v for i, v in enumerate(self._accepts)}

    def __call__(self, *args, **kwargs):
        varnames = self.varnames
        _typecheck_inputs(
            self._func.__name__,
            tuple(varnames.keys()),
            tuple(varnames.values()),
            args,
            kwargs
            )
        result = self._func(*args, **kwargs)
        result = _typecheck_output(
            self._func.__name__,
            self._returns,
            result
            )
        return result
