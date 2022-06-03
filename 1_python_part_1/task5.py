"""
Write function which receives line of space sepparated words.
Remove all duplicated words from line.
Restriction:
Examples:
    >>> remove_duplicated_words('cat cat dog 1 dog 2')
    'cat dog 1 2'
    >>> remove_duplicated_words('cat cat cat')
    'cat'
    >>> remove_duplicated_words('1 2 3')
    '1 2 3'
"""


def remove_duplicated_words(line: str) -> str:
    """Function which receives line of space separated words and
    removes all duplicated words from line."""

    tab_line = []

    for item in line.split(' '):
        if item not in tab_line:
            tab_line.append(item)

    return ' '.join(tab_line)
