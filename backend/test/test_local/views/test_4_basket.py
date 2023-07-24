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
    def test_auth(self, client):
        response = client.post('/auth/login', json={"email": "user@mail.ru"})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Вход тестового пользователя выполнен успешно'}

    def test_basket_get_empty(self, client):
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

    def test_basket_buy_get_empty(self, client):
        response = client.get('/basket/buy')

        assert response.status_code == 200
        assert response.get_json() == {'amount': 0,
                                       'data': 'Корзина пустая',
                                       'image': None,
                                       'name': None,
                                       'order_id': 0,
                                       'price': 0}

    def test_basket_patch_not_found(self, client):
        response = client.patch('/basket/', json={'card_id': 112000})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Такой товар не существует'}

    def test_basket_delete_not_found(self, client):
        response = client.delete('/basket/', json={'card_id': 112000})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'В вашей корзине нет такого товара'}

    def test_basket_patch_success(self, client):
        response = client.patch('/basket/', json={'card_id': 1})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Товар блины с мясом добавлен в корзину'}

    def test_basket_delete_success(self, client):
        response = client.delete('/basket/', json={'card_id': 1})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Товар удален из корзины'}

    def test_basket_patch_success_2(self, client):
        response = client.patch('/basket/', json={'card_id': 1})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Товар блины с мясом добавлен в корзину'}

    def test_basket_patch_success_3(self, client):
        response = client.patch('/basket/', json={'card_id': 2})

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Товар булочка с вишней добавлен в корзину'}

    def test_basket_get_full(self, client):
        response = client.get('/basket/')

        assert response.status_code == 200
        assert response.get_json() == [{'amount': 1,
                                        'card_id': 1,
                                        'data': None,
                                        'image': 'блины с мясом.jpeg',
                                        'name': 'блины с мясом',
                                        'order_id': 12,
                                        'price': 100,
                                        'user_id': 8},
                                       {'amount': 1,
                                        'card_id': 2,
                                        'data': None,
                                        'image': 'булочка с вишней.jpeg',
                                        'name': 'булочка с вишней',
                                        'order_id': 12,
                                        'price': 200,
                                        'user_id': 8}]

    def test_basket_buy_get_full(self, client):
        response = client.get('/basket/buy')

        assert response.status_code == 200
        assert response.get_json() == [{'amount': 1,
                                        'data': None,
                                        'image': 'блины с мясом.jpeg',
                                        'name': 'блины с мясом',
                                        'order_id': 12,
                                        'price': 100},
                                       {'amount': 1,
                                        'data': None,
                                        'image': 'булочка с вишней.jpeg',
                                        'name': 'булочка с вишней',
                                        'order_id': 12,
                                        'price': 200}]

    def test_auth_logout(self, client):
        response = client.get('/auth/logout')
