"""
Write function which receives filename and reads file line by line and returns min and mix integer from file.
Restriction: filename always valid, each line of file contains valid integer value
Examples:
    # file contains following lines:
        10
        -2
        0
        34
    >>> get_min_max('filename.txt') # I added .txt because it's impossible to do it without it. If I'm wrong, correct me.
    (-2, 34)
"""
from typing import Tuple


# I had to delete Hint section above, because it didn't work with it.


def get_min_max(filename: str) -> Tuple[int, int]:
    """Function which receives filename and reads the file line by line
     and returns min and max integer from the file."""

    minim = None
    maxim = None

    with open(filename) as opened_file:
        for line in opened_file:

            if minim == None or minim > int(line):
                minim = int(line)
            if maxim == None or maxim < int(line):
                maxim = int(line)

    return (minim, maxim)
