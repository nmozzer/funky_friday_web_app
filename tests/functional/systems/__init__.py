import pytest
from project import create_app, db
from project.models import System


@pytest.fixture(scope="module")
def client():
    app = create_app(True)
    with app.test_client() as client:
        with app.app_context():
            print(app.config)
            yield client


@pytest.fixture(scope="function")
def init_system_database(client):
    db.create_all()

    name = "TestyMcTestSystem"
    system_health = "Healthy"
    priority = 5
    language = "Perl"
    tech_stack = "MAWS"
    description = "A very old system"

    system = System(
        name=name,
        system_health=system_health,
        priority=priority,
        language=language,
        tech_stack=tech_stack,
        description=description,
    )

    db.session.add(system)
    db.session.commit()
    yield

    db.drop_all()
