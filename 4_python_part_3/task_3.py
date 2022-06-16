"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    #>>> is_http_domain('http://wikipedia.org')
    True
    #>>> is_http_domain('https://ru.wikipedia.org/')
    True
    #>>> is_http_domain('griddynamics.com')
    False
"""
import re
import pytest


def is_http_domain(domain: str) -> bool:
    if re.match(r"^http:/", domain):
        return True
    elif re.match(r"^https:/", domain):
        return True
    else:
        return False


"""
write tests for is_http_domain function
"""

domain_products =[
    ('http://wikipedia.org', True),
    ('https://ru.wikipedia.org/', True),
    ('griddynamics.com', False)
]


@pytest.mark.parametrize('domain, product', domain_products)
def test_is_http_domain(domain, product):
    assert is_http_domain(domain) == product
