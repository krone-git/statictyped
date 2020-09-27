from lib import *       # Imports 'statictyped', 'accepts', and 'returns'
                        # decorators and tuple-of-types constant, 'NUMERIC'
                        # (int, float);
from collections.abc import Iterable


@statictyped    # 'statictyped' decorator allows for declaring of static typed
                # parameters using function annotations;
def test(a: NUMERIC, b: str="b", *, c: Iterable=()) -> float:
    """test doc"""          # Original '__doc__' string;
    return a * 0.01

print("wrapper", test)                          # Displays the wrapper
                                                # function;
print("wrapped", test.base())                   # Displays the wrapped
                                                # function;
print("accepts", test.accepts())                # Displays the acceptable
                                                # datatypes with varnames;
print("returns", test.returns(), end="\n\n")    # Displays the returned
                                                # datatype;

help(test)          # Displays the 'help()' documentation for wrapper
                    # function. Notice the retained '__doc__' string from
                    # the original wrapped function with automatic parameter
                    # and return datatype documentation;

print("Valid", test(1))         # Display the results of call to wrapper
                                # function with proper datatypes;

print("Invalid", test("a"))     # Call with incorrect datatypes raises
                                # 'StaticTypeError';
