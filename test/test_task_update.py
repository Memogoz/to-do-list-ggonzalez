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
    assert task_x.tittle == 'New title'
    assert task_x.details == 'New details'
    assert task_x.priority == '5'

def test_markdown_procesing_and_sanitization_on_updates(client):
    client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'3','user_id':'100'})

    task = Task.query.get_or_404(1)
    task.title = '**New bold title**'
    task.details = '**New bold details**'
    task.priority = '5'
    db.session.commit()
    
    
    task = Task.query.first()
    assert task.tittle == '<p><strong>New bold title<p><strong>'
    assert task.details == '<p><strong>New bold details<p><strong>'

def test_timestamp_update_verification(client):
    client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'3','user_id':'100'})

    task = Task.query.get_or_404(1)
    date1 = task.date_created.date()

    task.title = 'New title'
    task.details = 'New details'
    task.priority = '5'
    db.session.commit()

    task_x = Task.query.first()
    date2 = task_x.date_created.date()

    assert date1 != date2

def test_invalid_imputs_or_unauthorized_access(client):
    client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'3','user_id':'100'})

    task = Task.query.get_or_404(1)
    task.title = 128
    task.details = 9348
    task.priority = 'string priority'

    commit_successful = False
        
    try:
        db.session.commit()
        commit_successful = True
    except:
        db.session.rollback()

    assert commit_successful == True

