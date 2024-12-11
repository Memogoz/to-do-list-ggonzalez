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
    task = Task.query.first()
    assert 'Test Task' == task.title

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
    task = Task.query.get_or_404(new_task.id)
    print('----------------',task.title,'------------------------')
    assert response.status_code == 302
    assert task.title == 'Test Task'
    assert task.details == 'Test Details'
    assert task.priority == 1

def test_delete_task(test_client, db_session, new_user, new_task):
    db_session.add(new_user)
    db_session.commit()
    db_session.add(new_task)
    db_session.commit()

    task = Task.query.first()
    response = test_client.get(f'/delete/{new_task.id}')
    assert response.status_code == 302

