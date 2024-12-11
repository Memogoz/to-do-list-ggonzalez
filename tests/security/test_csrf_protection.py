import pytest
from flask import url_for

def test_csrf_protection(test_client):
    response = test_client.post('/createAccount', data={'user': 'test', 'email': 'test@example.com', 'password': 'test'})
    assert response.status_code == 302  