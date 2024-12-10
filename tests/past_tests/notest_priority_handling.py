from flask import url_for
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


def test_correct_priority_assignment(client):
    client.post(url_for('app.todo'), data={'title':'Example title','details':'Example details','priority':'3','user_id':'100'})

    task = Task.query.get_or_404(1)
    assert task_x.priority == '3'

    task.title = 'New title'
    task.details = 'New details'
    task.priority = '5'
    db.session.commit()

    task_x = Task.query.first(client)
    assert task_x.priority == '5'

def test_proper_priority_ordering(client):
    pass #Not implemented