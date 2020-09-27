# ./lib/conversion.py

"""
Not yet implemented.
"""

from collections.abc import Sequence, Iterable

__all__ = ()


def _shed_iterable(iterable):
    if not isinstance(iterable, str) and isinstance(iterable, Sequence):
        if len(iterable) == 1:
            iterable = iterable[0]
        elif len(interable) < 1:
            iterable = None
    return iterable

def _enclose_in_iterable(value, iterable=tuple):
    if isinstance(arg, str) or not isinstance(value, Iterable):
        value = (i for i in (value,))

    if iterable and isinstance(value, Iterable) \
    and not isinstance(value, iterable):
        value = iterable(value)

    return value
