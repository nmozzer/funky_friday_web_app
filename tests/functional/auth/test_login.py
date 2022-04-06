from . import client, init_test_database
from flask_login import login_user
from project.models import User

def test_login(client, init_test_database):
    response = client.get('/login')
    assert response.status_code == 200


def test_login_post(client, init_test_database): 
    init_test_database   
    loginResponse = client.post('/login', data=dict(email='test@test.com', password='testPassword'), follow_redirects=True)

    assert loginResponse.status_code == 200
    assert b'Login' in loginResponse.data

def test_signup(client):
    response = client.get('/signup')

    assert response.status_code == 200
    assert b'Sign Up' in response.data

def test_signup_post(client, init_test_database):
    response = client.post('/signup', data=dict(email='moretest@test.com', password='testPassword', name='TestFace', type='user'), follow_redirects=True)

    assert response.status_code == 200

def test_signout(client, init_test_database):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data
