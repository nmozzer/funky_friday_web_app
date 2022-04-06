from . import client

def test_landing(client): 
    response = client.get('/', follow_redirects=True)

    # Check we are redirected to the login page
    assert b'View Systems' in response.data
