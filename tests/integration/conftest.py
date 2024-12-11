import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import create_app, db
from app.models.models import User, Task
from unittest.mock import patch

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test_secret'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def db_session(test_client):
    with test_client.application.app_context():
        yield db.session

@pytest.fixture
def mock_oauth_provider():
    with patch('app.routes.oauth.get_google_provider_cfg') as mock_google:
        mock_google.return_value = {
            "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo"
        }
        yield mock_google

@pytest.fixture
def new_user():
    return User(username='test_user', email='test@example.com', password='secure_password')

@pytest.fixture
def new_task(new_user):
    return Task(title='Test Task', details='Test Details', user_id=111)
