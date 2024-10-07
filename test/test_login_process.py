import pytest
from flask import url_for, request
from app import User, Task, app, db


def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_password_hashing_and_verification_process(client):
    pass #Not implemented

def test_session_management(client):
    user = User(username='testUser',email='test@email.com',password='testPassword')
    db.session.add(user)
    db.session.commit()
    client.post(url_for('app.login'), data={'user': 'testuser', 'password': 'testPassword'})

    User = User.query.first()
    assert User.user_id == '1'
    assert User.username == 'testUser'
    assert User.email == 'test@email.com'
    assert User.password == 'testPassword'

def test_error_handling_for_invalid_credentials(client):
    user = User(username='testUser',email='test@email.com',password='testPassword')
    db.session.add(user)
    db.session.commit()

    response = client.post(url_for('app.login'), data={'user': 'testuser', 'password': 'wrongPassword'})
    assert response.status_code == 401


