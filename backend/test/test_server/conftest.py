import pytest

# ты можешь менять этот url
CONFIG_TEST = 'https://tework123.ru/'


@pytest.fixture(scope='session', autouse=True)
def url_for_test():
    return CONFIG_TEST
