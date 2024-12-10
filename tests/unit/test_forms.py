'''import pytest
from app.forms import LoginForm, TaskForm

def test_login_form_validation():
    form = LoginForm(data={'username': 'testUser', 'password': 'testPassword'})
    assert form.validate() is True

    form_invalid = LoginForm(data={'username': '', 'password': ''})
    assert form_invalid.validate() is False

def test_task_form_validation():
    form = TaskForm(data={'title': 'Task Title', 'description': 'Task Description', 'status': 'Pending'})
    assert form.validate() is True

    form_invalid = TaskForm(data={'title': '', 'description': '', 'status': ''})
    assert form_invalid.validate() is False
'''