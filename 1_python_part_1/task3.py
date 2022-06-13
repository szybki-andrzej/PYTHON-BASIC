"""
Write function which receives list of text lines (which is space separated words) and word number.
It should enumerate unique words from each line and then build string from all words of given number.
Restriction: word_number >= 0
Examples:
    >>> build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1)
    'b 2 dog'
    >>> build_from_unique_words('a b c', '', 'cat dog milk', word_number=0)
    'a cat'
    >>> build_from_unique_words('1 2', '1 2 3', word_number=10)
    ''
    >>> build_from_unique_words(word_number=10)
    ''
"""
from typing import Iterable
from collections import OrderedDict


def build_from_unique_words(*lines: Iterable[str], word_number: int) -> str:
    """Function which receives list of text lines (which is space separated
    words) and word number and enumerate unique words from each line and the
    build string from all words of given number."""

    if word_number < 0:
        raise ValueError('word_number has to be more or equal to 0!')

    words_tab = \
        [list(OrderedDict.fromkeys(line.split(' '))) for line in lines if len(line) != 0]
    word_number_tab = \
        [item[word_number] for item in words_tab if len(item) > word_number]

    return ' '.join(word_number_tab)
