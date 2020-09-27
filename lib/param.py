# ./lib/param.py

"""
Not yet implemented.
"""


from functools import wraps

from .type import _typecheck_accepts, _typecheck_returns

from .func import _func_base, _func_name, _func_varnames, _func_annotations, \
                    WRAPPED_STATIC_FUNCTION

from .conversion import _shed_iterable


__all__ = ()

DEFAULT_TYPE = object

RETURN = "return"
ACCEPTS_STATIC_TYPES = "__acceptsstatictypes__"
RETURNS_STATIC_TYPE = "__returnstaticstype__"
IS_STATIC_TYPED_FUNCTION = "__isstatictypedfunction__"
ACCEPTS_DOC_STRING = "__acceptsdocstring__"
RETURNS_DOC_STRING = "__returnsdocstring__"

GET_ACCEPTS = "accepts"
GET_RETURNS = "returns"
GET_BASE = "base"
GET_VARNAMES = "varnames"

STATICTYPE_VARNAMES = (
    ACCEPTS_STATIC_TYPES,
    RETURNS_STATIC_TYPE,
    IS_STATIC_TYPED_FUNCTION,
    ACCEPTS_DOC_STRING,
    RETURNS_DOC_STRING,
    GET_ACCEPTS,
    GET_RETURNS,
    GET_BASE
    )


def _set_accepts(func, accepts):
    @wraps(func)
    def _accepts(*args, **kwargs):
        _typecheck_accepts(func, accepts, args, kwargs)
        return func(*args, **kwargs)
    _set_func_vars(_accepts, func, accepts, None)
    _set_accepts_docstring(_accepts, accepts)
    return _accepts

def _set_returns(func, returns):
    @wraps(func)
    def _returns(*args, **kwargs):
        result = func(*args, **kwargs)
        _typecheck_returns(func, returns, result)
        return result
    _set_func_vars(_returns, func, None, returns)
    _set_returns_doc_string(_returns, returns)
    return _returns

def _set_func_vars(func, base, accepts, returns):
    _set_is_statictyped(func)
    _set_base_func(func, base)
    _set_accepts_vars(func, base, accepts)
    _set_returns_vars(func, base, returns)
    if getattr(base, IS_STATIC_TYPED_FUNCTION, False):
        _del_func_vars(base)
    return func

def _set_accepts_vars(func, base, accepts):
    if not accepts:
        accepts = getattr(base, ACCEPTS_STATIC_TYPES, dict())
    setattr(func, ACCEPTS_STATIC_TYPES, accepts)
    setattr(func, GET_ACCEPTS, lambda: accepts)
    return func

def _set_returns_vars(func, base, returns):
    if not returns:
        returns = getattr(base, RETURNS_STATIC_TYPE, DEFAULT_TYPE)
    setattr(func, RETURNS_STATIC_TYPE, returns)
    setattr(func, GET_RETURNS, lambda: returns)
    return func

def _set_base_func(func, base):
    base = _func_base(base)
    setattr(func, WRAPPED_STATIC_FUNCTION, base)
    setattr(func, GET_BASE, lambda: base)
    return func

def _set_is_statictyped(func):
    setattr(func, IS_STATIC_TYPED_FUNCTION, True)
    return func

def _set_accepts_docstring(func, accepts):
    doc = "\n\n" + _new_accepts_doc_string(func, accepts)
    setattr(func, ACCEPTS_DOC_STRING, doc)
    returns_doc = getattr(func, RETURNS_DOC_STRING, "")
    func.__doc__ = func.__doc__.replace(returns_doc, "") \
                    + "\n\n" + "\n".join((doc.strip(), returns_doc.strip()))
    return func

def _new_accepts_doc_string(func, accepts):
    params = (
        f"param: '{k}'" + (f" {v}" if v else "") for k, v in accepts.items()
        )
    return "\n".join(params)

def _set_returns_doc_string(func, returns):
    accepts_doc = getattr(func, ACCEPTS_DOC_STRING, "")
    doc = ("" if accepts_doc else "\n\n") \
            + _new_returns_doc_string(func, returns)
    setattr(func, RETURNS_DOC_STRING, doc)
    func.__doc__ += doc
    return func

def _new_returns_doc_string(func, returns):
    return f"returns: {_shed_iterable(returns)}"

def _del_func_vars(func):
    for varname in STATICTYPE_VARNAMES:
        if hasattr(func, varname):
            delattr(func, varname)

def _accepts_from_declared(func, dtypes, kwdtypes):
    func = getattr(func, WRAPPED_STATIC_FUNCTION, func)
    varnames = _func_varnames(func)
    invalid_args = set(kwdtypes.keys()).difference(set(varnames))
    if len(invalid_args) > 0:
        raise NameError(
            f"Incorrect parameter names '{tuple(invalid_args)}' were given."
            )
    return {
        var: dtypes[i] if i < len(dtypes) \
        else kwdtypes.get(var, DEFAULT_TYPE) for i, var in enumerate(varnames)
        }

def _accepts_from_annotations(func):
    return {
        var: _func_annotations(func).get(var, DEFAULT_TYPE) \
        for var in _func_varnames(func)
        }

def _returns_from_annotations(func):
    returns = _func_annotations(func).get(RETURN)
    return (
        DEFAULT_TYPE if returns is None else returns,
        )
