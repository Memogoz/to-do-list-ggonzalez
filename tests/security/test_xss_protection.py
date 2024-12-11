import pytest
from flask import url_for


def test_xss_protection(test_client):
    payload = "<script>alert('XSS')</script>"
    response = test_client.post('/todo', data={'title': payload, 'details': 'XSS Test', 'priority': 1})
    assert payload not in response.data.decode()  