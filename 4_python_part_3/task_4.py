"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import sys
from unittest import mock
from faker import Faker


def print_name_address(args: argparse.Namespace) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument('number', type=int)
    parser.add_argument('--fake-address')
    parser.add_argument('--some-name')

    args = parser.parse_args()
    string_placeholder = ''

    for i in range(args.number):
        fake_dict = {}
        faker = Faker()
        if args.some_name:
            fake_dict['some-name'] = faker.name()
        if args.fake_address:
            fake_dict['fake-address'] = faker.address()
        string_placeholder = string_placeholder + str(fake_dict) + '\n'
    print(string_placeholder)
    return string_placeholder


if __name__ == "__main__":
    print_name_address(sys.argv[1:])

"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(number=2, fake_address='address', some_name='name'))
def test_print_name_address(mock_args):

    split_result = list(print_name_address(mock_args).split('\n'))
    split_result.pop()

    for result in split_result:
        result_dict_keys = [*eval(result)]
        assert result_dict_keys[0] == 'some-name'
        assert result_dict_keys[1] == 'fake-address'

