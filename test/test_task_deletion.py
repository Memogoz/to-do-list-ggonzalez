import pytest
from flask import url_for
from app import User, Task, app, db


def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_autorization():
    pass #Not implemeted

def test_task_removed_from_database(client):
    client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'3','user_id':'100'})
    response = client.post(url_for('app.delete'), data={'id':1})
    task = Task.query.first()
    assert task == None

def test_task_not_found(client):
    client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'3','user_id':'100'})
    response = client.post(url_for('app.delete'), data={'id':99})
    assert response == 'There was a problem deleting that task'