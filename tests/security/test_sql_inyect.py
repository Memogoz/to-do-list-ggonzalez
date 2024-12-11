import pytest
from flask import url_for


def test_sql_injection(test_client):
    payload = "' OR 1=1 --"
    response = test_client.post('/login', data={'user': payload, 'password': 'irrelevant'})
    assert b'Redirecting' in response.data 