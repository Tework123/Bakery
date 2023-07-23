import pytest


@pytest.mark.usefixtures('client')
class TestProfileUnauthorized:

    def test_profile_current_orders_get(self, client):
        response = client.get('/profile/current_orders')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_profile_pass_orders_get(self, client):
        response = client.get('/profile/pass_orders')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}


@pytest.mark.usefixtures('client')
class TestProfileAuthorized:

    def test_auth(self, client):
        response = client.post('/auth/login', json={"email": "user@mail.ru"})

    def test_profile_current_orders_get(self, client):
        response = client.get('/profile/current_orders')

        assert response.status_code == 200
        assert response.get_json() == [{'address': None,
                                        'amount': '1, 1',
                                        'date': response.get_json()[0]['date'],
                                        'name': 'блины с мясом, булочка с вишней',
                                        'order_id': 12,
                                        'status': 'paid',
                                        'text': None}]

    def test_profile_pass_orders_get(self, client):
        response = client.get('/profile/pass_orders')

        assert response.status_code == 200
        assert response.get_json() == []

    def test_profile_pass_orders_1_get(self, client):
        response = client.get('/profile/pass_orders/1')

        assert response.status_code == 200
        assert response.get_json() == {'amount': None,
                                       'data': 'У вас нет такого заказа',
                                       'name': None,
                                       'order_id': 0,
                                       'price': 0,
                                       'status': None}

    def test_auth_logout(self, client):
        response = client.get('/auth/logout')
