import pytest


@pytest.mark.usefixtures('client')
class TestProfileUnauthorized:

    def test_profile_orders_get(self, client):
        response = client.get('/profile/orders')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_profile_get(self, client):
        response = client.get('/profile/')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}


@pytest.mark.usefixtures('client')
class TestProfileAuthorized:

    def test_auth(self, client):
        response = client.post('/auth/login', json={"email": "user@mail.ru"})

    def test_profile_orders_get(self, client):
        response = client.get('/profile/orders')

        assert response.status_code == 200
        assert response.get_json() == [{'cards': [{'amount': 1,
                                                   'image': '/static/%D0%B1%D0%BB%D0%B8%D0%BD%D1%8B%20%D1%81%20%D0%BC%D1%8F%D1%81%D0%BE%D0%BC.jpeg',
                                                   'name': 'блины с мясом'},
                                                  {'amount': 1,
                                                   'image': '/static/%D0%B1%D1%83%D0%BB%D0%BE%D1%87%D0%BA%D0%B0%20%D1%81%20%D0%B2%D0%B8%D1%88%D0%BD%D0%B5%D0%B9.jpeg',
                                                   'name': 'булочка с вишней'}],
                                        'date': response.get_json()[0]['date'],
                                        'order_id': 13,
                                        'price': 300,
                                        'status': 'paid',
                                        'text': None}]

    def test_profile_pass_orders_1_get(self, client):
        response = client.get('/profile/orders/1')

        assert response.status_code == 200
        assert response.get_json() == {'amount': None,
                                       'data': 'У вас нет такого заказа',
                                       'image': None,
                                       'name': None,
                                       'order_id': 0,
                                       'price': 0,
                                       'status': None}

    def test_auth_logout(self, client):
        response = client.get('/auth/logout')
