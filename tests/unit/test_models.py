import pytest
from app import User, Task, db, create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_user_task_relationship(client):
    user = User(username='testUser', email='test@example.com', password='testPassword')
    task = Task(title="Test Task", details="Task Description", user=user)
    db.session.add(user)
    db.session.add(task)
    db.session.commit()

    # Verificar relación
    assert task.user_id == user.id
    assert user.tasks[0].title == "Test Task"
