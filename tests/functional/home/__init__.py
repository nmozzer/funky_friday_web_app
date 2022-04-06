import pytest
from project import create_app

@pytest.fixture(scope='module')
def client():
    app = create_app(True)

    with app.test_client() as client:
        with app.app_context():
            yield client

