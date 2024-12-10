import pytest

def test_user_authentication_and_task_workflow(test_client, db_session):
    # Registrar un usuario
    response = test_client.post('/createAccount', data={
        'user': 'test_user',
        'email': 'test@example.com',
        'password': 'secure_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

    # Iniciar sesión
    response = test_client.post('/login', data={
        'user': 'test_user',
        'password': 'secure_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back' in response.data

    # Crear una tarea
    response = test_client.post('/todo', data={
        'title': 'Integration Test Task',
        'details': 'Testing task workflow',
        'priority': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Integration Test Task' in response.data

    # Actualizar la tarea
    response = test_client.post('/update/1', data={
        'title': 'Updated Integration Task',
        'details': 'Updated task details',
        'priority': 2
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Integration Task' in response.data

    # Eliminar la tarea
    response = test_client.get('/delete/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Updated Integration Task' not in response.data
