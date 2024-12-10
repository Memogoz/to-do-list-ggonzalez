import pytest
from app.models.models import User, Task

def test_database_operations(db_session):
    # Crear un usuario
    user = User(username='test_user', email='test@example.com', password='secure_password')
    db_session.add(user)
    db_session.commit()
    assert User.query.count() == 1

    # Crear una tarea
    task = Task(title='Test Task', details='Test Details', user_id=user.id)
    db_session.add(task)
    db_session.commit()
    assert Task.query.count() == 1

    # Relación entre usuario y tareas
    user_tasks = User.query.get(user.id).tasks
    assert len(user_tasks) == 1
    assert user_tasks[0].title == 'Test Task'
