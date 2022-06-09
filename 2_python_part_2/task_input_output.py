"""
Write function which reads a number from input nth times.
If an entered value isn't a number, ignore it.
After all inputs are entered, calculate an average entered number.
Return string with following format:
If average exists, return: "Avg: X", where X is avg value which rounded to 2 places after the decimal
If it doesn't exist, return: "No numbers entered"
Examples:
    user enters: 1, 2, hello, 2, world
    >>> read_numbers(5)
    Avg: 1.67
    ------------
    user enters: hello, world, foo, bar, baz
    >>> read_numbers(5)
    No numbers entered
"""
import numpy as np


def read_numbers(n: int) -> str:
    numbers_tab = []

    for i in range(n):
        try:
            numbers_tab.append(float(input("Enter the number")))
        except ValueError:
            pass  # I'm using pass statement because as it is sad above I
            # don't need to do anything when ValueError occurs

    if len(numbers_tab) > 0:
        return round(np.mean(numbers_tab), 2)

    else:
        print("No numbers entered")
