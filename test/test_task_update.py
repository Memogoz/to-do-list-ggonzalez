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


def test_correct_update(client):    
    client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'3','user_id':'100'})

    task = Task.query.get_or_404(1)
    task.title = 'New title'
    task.details = 'New details'
    task.priority = '5'
    db.session.commit()

    task_x = Task.query.first()
    assert (task_x.tittle == 'New title' and task_x.details == 'New details' and task_x.priority == '5')


def test_markdown_procesing_and_sanitization_on_updates():
    pass

def test_timestamp_update_verification():
    pass

def test_invalid_imputs_or_unauthorized_access():
    pass