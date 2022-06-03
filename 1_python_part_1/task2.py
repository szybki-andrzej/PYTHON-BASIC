"""
Write function which updates dictionary with defined values but only if new value more than in dict
Restriction: do not use .update() method of dictionary
Examples:
    >>> set_to_dict({'a': 1, 'b': 2, 'c': 3}, a=0, b=4)  # only b updated because new value for a less than original value
    {'a': 1, 'b': 4, 'c': 3}
    >>> set_to_dict({}, a=0) # for no reason there was no quotation marks around a and I added it. Correct me if it was wrong.
    {'a': 0}
    >>> set_to_dict({'a': 5})
    {'a': 5}
"""
from typing import Dict


def set_to_dict(dict_to_update: Dict[str, int], **items_to_set) -> Dict:
    """Function which updates dictionary with defined values but only if new value more than in dict."""

    for i in items_to_set:
        if i not in dict_to_update or dict_to_update[i] < items_to_set[i]:
            dict_to_update[i] = items_to_set[i]

    return dict_to_update
