import pytest
from app.models.models import Task

def test_create_task(db_session, new_user, new_task):
    db_session.add(new_user)
    db_session.commit()
    db_session.add(new_task)
    db_session.commit()
    task = Task.query.filter_by(title='Test Task').first()
    assert task is not None
    assert task.details == 'Test Details'

def test_read_task(test_client, db_session, new_user, new_task):
    db_session.add(new_user)
    db_session.commit()
    db_session.add(new_task)
    db_session.commit()
    response = test_client.get('/todo')
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_update_task(test_client, db_session, new_user, new_task):
    db_session.add(new_user)
    db_session.commit()
    db_session.add(new_task)
    db_session.commit()

    response = test_client.post(f'/update/{new_task.id}', data={
        'title': 'Updated Task',
        'details': 'Updated Details',
        'priority': 2
    })
    assert response.status_code == 302  # Redirige a /todo
    task = Task.query.get(new_task.id)
    assert task.title == 'Updated Task'
    assert task.details == 'Updated Details'
    assert task.priority == 2

def test_delete_task(test_client, db_session, new_user, new_task):
    db_session.add(new_user)
    db_session.commit()
    db_session.add(new_task)
    db_session.commit()

    response = test_client.get(f'/delete/{new_task.id}')
    assert response.status_code == 302  # Redirige a /todo
    task = Task.query.get(new_task.id)
    assert task is None
