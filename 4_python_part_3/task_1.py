"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
#    >>> calculate_days('2022-06-17')  # for this example today is 6 october 2021
    -1
#    >>> calculate_days('2022-06-15')
    1
#    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
from datetime import datetime, date
import pytest


def calculate_days(from_date: str) -> int:
    try:
        date_converted = datetime.strptime(from_date, '%Y-%m-%d').date()
        days = date.today() - date_converted
        return days.days

    except ValueError:
        print("WrongFormatException")


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""

products_correct_format = [
    ('2022-06-17', -1),
    ('2022-05-16', 31),
    ('2022-06-14', 2),
]

today_date = date(2022, 6, 16)


@pytest.mark.freeze_time('2022-06-16')
@pytest.mark.parametrize('custom_date, days', products_correct_format)
def test_calculate_days_correct_format(custom_date, days):
    assert calculate_days(custom_date) == days


def test_calculate_days_wrong_format(capfd):
    calculate_days('10-07-2021')

    out, err = capfd.readouterr()
    assert out == 'WrongFormatException\n'
