import pytest


@pytest.mark.usefixtures('client')
class TestBasketUnauthorized:

    def test_basket_get(self, client):
        response = client.get('/basket/')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_basket_buy_get(self, client):
        response = client.get('/basket/buy')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_basket_patch(self, client):
        response = client.patch('/basket/')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_basket_delete(self, client):
        response = client.delete('/basket/', json={'card_id': 1})

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}


@pytest.mark.usefixtures('client')
class TestBasketAuthorized:
    def test_main(self, client):
        response = client.post('/auth/login', json={"email": "user@mail.ru"})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Вход тестового пользователя выполнен успешно'}

    def test_basket_get(self, client):
        response = client.get('/basket/')

        assert response.status_code == 200
        assert response.get_json() == {'amount': 0,
                                       'card_id': 0,
                                       'data': 'Корзина пустая',
                                       'image': None,
                                       'name': None,
                                       'order_id': 0,
                                       'price': 0,
                                       'user_id': 0}

    def test_basket_buy_get(self, client):
        response = client.get('/basket/buy')

        assert response.status_code == 200
        assert response.get_json() == {'amount': 0,
                                       'data': 'Корзина пустая',
                                       'image': None,
                                       'name': None,
                                       'order_id': 0,
                                       'price': 0}

    def test_basket_patch(self, client):
        response = client.patch('/basket/', json={'card_id': 112000})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Такой товар не существует'}

    def test_basket_delete(self, client):
        response = client.delete('/basket/', json={'card_id': 112000})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'В вашей корзине нет такого товара'}

    def test_auth_logout(self, client):
        response = client.get('/auth/logout')
