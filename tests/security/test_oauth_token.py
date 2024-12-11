import pytest
from flask import url_for

from flask import session
from unittest.mock import patch
'''
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
            assert response.status_code == 200'''
