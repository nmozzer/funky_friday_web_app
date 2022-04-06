from . import client

def test_landing(client):
    landing = client.get('/')
    html = landing.data.decode()

    assert "<a href=\"\/\">Home</a>" in html
    assert " <a href=\"/profile/\">Profile</a>" in html
    assert landing.status_code == 200
