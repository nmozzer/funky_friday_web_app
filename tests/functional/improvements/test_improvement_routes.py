from . import client, init_improvement_database


def test_improvements(client, init_improvement_database):
    response = client.get("/improvements", follow_redirects=True)

    assert response.status_code == 200
    assert b"Migrate to Coral 3.0" in response.data


def test_view(client, init_improvement_database):
    response = client.get("/improvements/view?improvement_id=1", follow_redirects=True)

    assert response.status_code == 200

    assert b"Migrate to Coral 3.0" in response.data
    assert b"1" in response.data
    assert b"4" in response.data
    assert b"A great idea" in response.data


def test_create(client, init_improvement_database):
    response = client.get("/improvements/create?system_id=1", follow_redirects=True)

    assert response.status_code == 200

    assert b"Improvement Name" in response.data
    assert b"Add Improvement for TestyMcTestSystem" in response.data
    assert b"Number of Beans" in response.data
    assert b"Improvement Description" in response.data
    assert b"Submit" in response.data


def test_edit(client, init_improvement_database):
    response = client.get(
        "/improvements/edit?improvement_id=1&system_id=1", follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Improvement Name" in response.data
    assert b"Edit Improvement" in response.data
    assert b"Number of Beans" in response.data
    assert b"Improvement Description" in response.data
    assert b"Submit" in response.data

    assert b"Migrate to Coral 3.0" in response.data
    assert b"4" in response.data
