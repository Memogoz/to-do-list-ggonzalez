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


def test_create_task_valid_input(client):
    user = User(username='testUser',email='test@email.com',password='testPassword')
    db.session.add(user)
    db.session.commit()
    client.post(url_for('app.login'), data={'user': 'testuser', 'password': 'testPassword'})
    # Test
    response = client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'4','user_id':'100'})
    assert response.status_code == 302 # Redirect after successful creation
    
    task = Task.query.first()
    assert task is not None
    assert task.title == 'Example title'
    assert task.priority == '4'
    assert task.user_id == '100'

def test_empty_task(client):
    response = client.post(url_for('app.todo'), data={'title':'','details':'','priority':'','user_id':''})
    assert response == 'There was an issue adding your task'

def test_create_task_invalid_priority(client):
    response = client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'high','user_id':'100'})
    assert response == 'There was an issue adding your task'

def test_create_task_markdown_processing(client):
    response = client.post(url_for('app.todo'), data={'title':'**Bold title**','details':'Example details','priority':'3','user_id':'100'})
    task = Task.query.first()
    assert task.tittle == '<p><strong>Bold title<p><strong>'

def test_create_task_content_sanitization(client):
    response = client.post(url_for('app.todo'), data={'title':'<script>alert("title alert")script>','details':'Example details','priority':'3','user_id':'100'})
    task = Task.query.first()
    assert '<script>' not in task.content