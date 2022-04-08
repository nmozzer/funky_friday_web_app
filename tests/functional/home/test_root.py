from . import client


def test_landing(client):
    response = client.get("/", follow_redirects=True)

    assert response.status_code == 200
    assert b"View Systems" in response.data
