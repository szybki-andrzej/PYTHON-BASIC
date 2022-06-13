"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value, and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3]) # I had to delete the comment below because it didn't work with it.
    [1, 4, 7]
"""
from typing import List


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    """Function which receives list of integers calculating power of each
     integer and subtracting difference between original previous value,
     and it's power. For first value subtracts nothing."""

    power_dict = {ints[0]: ints[0] ** 2}
    result_tab = [power_dict[ints[0]]]

    for i in range(1, len(ints)):
        power_dict[i+1] = (i+1)**2
        result_tab.append(power_dict[i+1] - power_dict[i] + ints[i-1])

    return result_tab
