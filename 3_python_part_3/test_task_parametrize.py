"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.
Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number
Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""

import pytest


def fibonacci_1(n):
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a + b
    return b


def fibonacci_2(n):
    fibo = [0, 1]
    for i in range(2, n+1):
        fibo.append(fibo[i-1] + fibo[i-2])
    return fibo[n]


products = [
    (1, 1),
    (2, 1),
    (4, 3),
    (5, 5),
    (9, 34),
    (11, 89),
    (20, 6765)
]


@pytest.mark.parametrize('n, product', products)
def test_fibonacci_1(n, product):
    assert fibonacci_1(n) == product


@pytest.mark.parametrize('n, product', products)
def test_fibonacci_2(n, product):
    assert fibonacci_2(n) == product
