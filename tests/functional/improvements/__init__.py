import pytest
from project import create_app, db
from project.models import Improvement, System

@pytest.fixture(scope='module')
def client():
    app = create_app(True)
    with app.test_client() as client:
        with app.app_context():
            print(app.config)
            yield client

@pytest.fixture(scope='function')
def init_improvement_database(client):
    db.create_all()
    name = 'Migrate to Coral 3.0'
    system_id = 1
    beans = 4
    user_id = 1
    description = 'A great idea'

    improvement = Improvement(name=name, system_id=system_id, beans=beans, user_id=user_id, description=description)

    name = 'TestyMcTestSystem'
    system_health = 'Healthy'
    priority = 5
    language = 'Perl'
    tech_stack = 'MAWS'
    description = 'A very old system'
    
    system = System(name=name, system_health=system_health, priority=priority, language=language, tech_stack=tech_stack, description=description)

    db.session.add(system)
    db.session.add(improvement)
    db.session.commit()
    yield

    db.drop_all()
