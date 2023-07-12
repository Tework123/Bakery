import pytest

from application import create_app, db
from config import TestingConfig


@pytest.fixture(scope='session', autouse=True)
def app():
    _app = create_app(TestingConfig)
    app_context = _app.app_context()
    app_context.push()
    db.create_all()

    yield _app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture(scope='session')
def add_data_to_db(app):
    pass
