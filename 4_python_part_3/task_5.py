"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
#     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
import requests
from unittest.mock import Mock


def make_request(url: str) -> Tuple[int, str]:
    response = requests.get(url)
    status_code = response.status_code
    response.encoding = 'utf-8'
    return status_code, response.text


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""


def test_make_request():
    test_request = Mock()
    test_request.status_code.return_value = 200

    assert test_request.status_code() == make_request('https://www.google.com')[0]


