import pytest
from flask import session

def test_mock_oauth_flow(test_client, mock_oauth_provider):
    # Simula el flujo de OAuth
    response = test_client.get('/login/oauth', follow_redirects=True)
    assert response.status_code == 200
    assert b'Authorize Google' in response.data

    # Simula la respuesta de éxito del proveedor OAuth
    with test_client.session_transaction() as sess:
        sess['oauth_token'] = 'mock_token'
        sess['oauth_user'] = {'email': 'test_oauth@example.com', 'name': 'Test User'}
    
    response = test_client.get('/todo', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome Test User' in response.data
