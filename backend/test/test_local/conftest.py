import pytest

from application import create_app, db
from application.command.routes import add_users_base, add_cards_base, add_orders_base, add_for_test_users_base, \
    add_for_test_orders_base
from config import TestingConfig


# ДЛЯ РАБОТЫ ТЕСТОВ ОТКЛЮЧЕНА ОТПРАВКА ЕМАЙЛА, ТАК КАК ВЫДАЕТ ЦИРКУЛЯРНЫЙ ИМПОРТ, НАДО РЕШИТЬ ПРОБЛЕМУ
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
    add_users_base()

    add_cards_base()

    add_orders_base()


@pytest.fixture(scope='session')
def add_test_data_to_db(app):
    add_for_test_users_base()

    add_cards_base()

    add_for_test_orders_base()
