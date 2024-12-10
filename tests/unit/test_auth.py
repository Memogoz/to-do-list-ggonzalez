import pytest
from app.models.models import User

def test_create_user(db_session, new_user):
    db_session.add(new_user)
    db_session.commit()
    user = User.query.filter_by(username='test_user').first()
    assert user is not None
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'

def test_login_success(test_client, db_session, new_user):
    db_session.add(new_user)
    db_session.commit()
    response = test_client.post('/login', data={'user': 'test_user', 'password': 'secure_password'})
    assert response.status_code == 302  # Redirige a /todo

def test_login_failure(test_client):
    response = test_client.post('/login', data={'user': 'wrong_user', 'password': 'wrong_password'})
    assert response.status_code == 302  # Redirige a /login

def test_logout(test_client):
    with test_client.session_transaction() as session:
        session['logged_in'] = True
    response = test_client.get('/logout')
    assert response.status_code == 302  # Redirige a /
