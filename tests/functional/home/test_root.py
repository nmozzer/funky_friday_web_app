from . import client

def test_landing_not_logged_in(client):
    response = client.get('/')
    # User should be redirected if not logged in
    assert response.status_code == 302

    redirectResponse = client.get('/', follow_redirects=True)
    loginResponse = client.get('/login')

    # Check we are redirected to the login page
    assert redirectResponse.data == loginResponse.data
