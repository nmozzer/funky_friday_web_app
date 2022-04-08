from . import client, init_system_database


def test_systems(client, init_system_database):
    response = client.get("/systems", follow_redirects=True)

    assert response.status_code == 200
    assert b"Add a new System" in response.data
    assert b"TestyMcTestSystem" in response.data
    assert b"Edit" in response.data


def test_view(client, init_system_database):
    response = client.get("/systems/view?system_id=1", follow_redirects=True)

    assert response.status_code == 200

    assert b"TestyMcTestSystem" in response.data
    assert b"Perl" in response.data
    assert b"5" in response.data
    assert b"MAWS" in response.data
    assert b"A very old system" in response.data


def test_create(client, init_system_database):
    response = client.get("/systems/create", follow_redirects=True)

    assert response.status_code == 200

    assert b"Add System" in response.data
    assert b"System Health" in response.data
    assert b"System Language" in response.data
    assert b"Tech Stack" in response.data
    assert b"System Description" in response.data
    assert b"Submit" in response.data


def test_create_post(client, init_system_database):
    response = client.post(
        "/systems/create",
        data=dict(
            name="DifferentSystem",
            system_health="Unhealthy",
            priority=4,
            language="Java",
            description="An interesting description",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert b"TestyMcTestSystem" in response.data
    assert b"DifferentSystem" in response.data
    assert b"System Successfully Added" in response.data


def test_edit(client, init_system_database):
    response = client.get("/systems/edit?system_id=1", follow_redirects=True)

    assert response.status_code == 200

    assert b"Edit" in response.data
    assert b"System Health" in response.data
    assert b"System Language" in response.data
    assert b"Tech Stack" in response.data
    assert b"System Description" in response.data
    assert b"Submit" in response.data

    assert b"TestyMcTestSystem" in response.data
    assert b"Perl" in response.data
    assert b"5" in response.data
    assert b"MAWS" in response.data


def test_edit_post(client, init_system_database):
    response = client.post(
        "/systems/edit?system_id=1",
        data=dict(
            name="TestyMcTestFaceChanged",
            system_health="Unhealthy",
            priority=4,
            language="Java",
            description="An interesting description",
            system_id=1,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert b"TestyMcTestFaceChanged" in response.data
    assert b"System Successfully Edited" in response.data
