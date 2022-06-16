"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     #>>> math_calculate('log', 1024, 2)
     10.0
     #>>> math_calculate('ceil', 10.7)
     11
"""
import math


def math_calculate(function: str, *args):
    command_string = 'math.{}(*args)'.format(function)
    return eval(command_string)


"""
Write tests for math_calculate function
"""


def test_math_calculate():
    assert math_calculate('log', 1024, 2) == 10.0
    assert math_calculate('ceil', 10.7) == 11
    assert math_calculate('sqrt', 256) == 16
    assert math_calculate('pow', 2, 8) == 256



