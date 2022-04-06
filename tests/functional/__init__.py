import pytest
from project import create_app, db
from project.models import User


@pytest.fixture(scope='module')
def client():
    app = create_app(True)

    with app.test_client() as client:
        with app.app_context():
            yield client


# @pytest.fixture(scope='function')
# def init_test_database(client):
#     db.create_all()

#     email = 'test@test.com'
#     password ='testPassword'
#     name = 'TestyMcTestFace'
#     type = 'user'

#     user = User(name=name, password=password, email=email, type=type)
#     db.session.add(user)

#     db.session.commit()

#     yield

#     db.drop_all()
