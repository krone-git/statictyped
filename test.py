

from functools import wraps
from random import randint


# def testwrap(func):
#     @wraps(func)
#     def _test(*args):
#         return func(*arg)
#     _test.x = [randint(0, 100)]
#     return _test

class testwrap:
    def __init__(self, func):
        self._func = func
        wraps(func)(self)

    @property
    def accepts(self):
        return self._func.__code__.co_varnames

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


@testwrap
def test(a):
    """test doc"""
    return 0

class Class1:
    @testwrap
    def test1(b):
        """test1 doc"""
        return 1

    @testwrap
    def test2(c):
        """test2 doc"""
        return 2

    @testwrap
    def test3(d):
        """test3 doc"""
        return 3

c1 = Class1()

print(test.accepts)
print(c1.test1.accepts)
print(c1.test2.accepts)
print(c1.test3.accepts)
