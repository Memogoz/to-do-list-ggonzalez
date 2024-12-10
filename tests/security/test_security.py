import pytest
from flask import url_for

@pytest.fixture(scope="module")
def test_client():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sql_injection(test_client):
    payload = "' OR 1=1 --"
    response = test_client.post('/login', data={'user': payload, 'password': 'irrelevant'})
    assert b'Invalid credentials' in response.data  # El sistema debe manejarlo correctamente

def test_xss_protection(test_client):
    payload = "<script>alert('XSS')</script>"
    response = test_client.post('/todo', data={'title': payload, 'details': 'XSS Test', 'priority': 1})
    assert payload not in response.data.decode()  # El contenido no debe reflejarse sin sanitización

def test_csrf_protection(test_client):
    response = test_client.post('/createAccount', data={'user': 'test', 'email': 'test@example.com', 'password': 'test'})
    assert response.status_code == 403  # Si no se incluye un token CSRF válido, debería fallar

from flask import session

def test_session_hijacking_prevention(test_client):
    with test_client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['logged_in'] = True

    # Simular uso de sesión vencida
    test_client.get('/logout')
    response = test_client.get('/todo')
    assert b'Please log in' in response.data  # El sistema debe bloquear el acceso

from unittest.mock import patch

def test_oauth_token_validation(test_client):
    with patch('app.routes.oauth.get_google_provider_cfg') as mock_google:
        mock_google.return_value = {
            "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo"
        }
        with patch('app.routes.oauth.requests.post') as mock_post:
            mock_post.return_value.json.return_value = {'access_token': 'mock_token', 'id_token': 'mock_id'}
            response = test_client.get('/login/oauth', follow_redirects=True)
            assert response.status_code == 200
