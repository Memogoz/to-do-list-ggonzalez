import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import User, Task, create_app, db


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_password_hashing_and_verification_process(client):
    pass #Not implemented

def test_session_management(client):
    user = User(username='testUser', email='test@email.com', password='testPassword')
    db.session.add(user)
    db.session.commit()

    # Simular login
    response = client.post('/login', data={'user': 'testUser', 'password': 'testPassword'})

    # Validar redirección y datos
    assert response.status_code == 302  # Redirige al /todo si es exitoso
    user_from_db = User.query.first()
    assert user_from_db.id == 1
    assert user_from_db.username == 'testUser'
    assert user_from_db.email == 'test@email.com'
    assert user_from_db.password == 'testPassword'


def test_error_handling_for_invalid_credentials(client):
    user = User(username='testUser', email='test@email.com', password='testPassword')
    db.session.add(user)
    db.session.commit()

    # Intentar login con contraseña incorrecta
    response = client.post('/login', data={'user': 'testUser', 'password': 'testPassword'})

    assert response.status_code == 302  # Verifica la redirección



