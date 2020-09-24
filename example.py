from lib.accepts import statictyped, accepts, returns


@accepts(a=int)
@returns(str)
def test(a):
    """test doc"""
    return a * 0.01

test(1)
help(test)
