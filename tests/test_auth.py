import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a@a.a', 'password': 'a', 'password2': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']
    
    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a@a.a'",
        ).fetchone() is not None
        
@pytest.mark.parametrize(('username', 'password', 'password2', 'message'), (
    ('', '', '', b'Email is required.'),
    ('a', '', '', b'Please enter a valid email.'),
    ('a@a', '', '', b'Password is required.'),
    ('a@a', 'test', 't', b'are not the same.'),
    ('test@test.com', 'test', 'test', b'already registered')
))
def test_register_validate_input(client, username, password, password2, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'password2': password2}
    )
    assert message in response.data
    
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'
    
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test@test.com'
        
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test@test.com', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    
def test_logout(client, auth):
    auth.login()
    
    with client:
        auth.logout()
        assert 'user_id' not in session