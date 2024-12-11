import pytest
from flask import url_for
from flask import session

def test_session_hijacking_prevention(test_client):
    with test_client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['logged_in'] = True

    # Simular uso de sesión vencida
    test_client.get('/logout')
    response = test_client.get('/todo')
    assert b'Redirecting' in response.data  # El sistema debe bloquear el acceso
