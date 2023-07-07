import pytest

# ты можешь менять этот url
CONFIG_TEST = 'http://127.0.0.1:5000/'


@pytest.fixture(scope='session', autouse=True)
def url_for_test():
    return CONFIG_TEST
