import pytest

def test_login_form_validation(test_client):
    form_valid = test_client.post('/login', data={'user': 'test_user', 'password': 'secure_password'})
    assert form_valid.status_code == 302

    form_invalid = test_client.post('/login', data={'user': 'test_user', 'password': ''})
    assert form_invalid.status_code == 302

def test_task_form_validation(test_client):
    task_valid = test_client.post('/todo', data={'title': 'test_title', 'details': 'test_details','priority':3,})
    assert task_valid.status_code == 302

    task_invalid = test_client.post('/todo', data={'title': '', 'details': 'test_details','priority':3,})
    assert task_invalid.status_code == 302
