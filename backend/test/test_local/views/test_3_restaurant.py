import base64
import io

import pytest

from start_app import CONFIG


@pytest.mark.usefixtures('client')
class TestRestaurantUnauthorized:

    def test_restaurant_cards_get(self, client):
        response = client.get('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_cards_post(self, client):
        response = client.post('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_cards_patch(self, client):
        response = client.patch('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_cards_delete(self, client):
        response = client.delete('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_orders_get(self, client):
        response = client.get('/restaurant/orders')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_orders_patch(self, client):
        response = client.patch('/restaurant/orders')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}


@pytest.mark.usefixtures('client')
class TestRestaurantUnauthorized:

    def test_restaurant(self, client):
        response = client.post('/auth/login', json={"email": "restaurant@mail.ru"})

    # Не понятно, если вернет картинки, то что с ними делать, там же тоже не json будет
    def test_restaurant_cards_get(self, client):
        response = client.get('/restaurant/cards')

        assert response.status_code == 200
        assert response.get_json() == [{'card_id': 1,
                                        'image': '/static/%D0%B1%D0%BB%D0%B8%D0%BD%D1%8B%20%D1%81%20%D0%BC%D1%8F%D1%81%D0%BE%D0%BC.jpeg',
                                        'name': 'блины с мясом',
                                        'price': 100},
                                       {'card_id': 2,
                                        'image': '/static/%D0%B1%D1%83%D0%BB%D0%BE%D1%87%D0%BA%D0%B0%20%D1%81%20%D0%B2%D0%B8%D1%88%D0%BD%D0%B5%D0%B9.jpeg',
                                        'name': 'булочка с вишней',
                                        'price': 200},
                                       {'card_id': 3,
                                        'image': '/static/%D0%B1%D1%83%D0%BB%D0%BE%D1%87%D0%BA%D0%B0%20%D1%81%20%D0%B8%D0%B7%D1%8E%D0%BC%D0%BE%D0%BC.jpeg',
                                        'name': 'булочка с изюмом',
                                        'price': 150},
                                       {'card_id': 4,
                                        'image': '/static/%D0%B1%D1%83%D0%BB%D0%BE%D1%87%D0%BA%D0%B0%20%D1%81%20%D0%BA%D0%BB%D1%83%D0%B1%D0%BD%D0%B8%D0%BA%D0%BE%D0%B9.jpeg',
                                        'name': 'булочка с клубникой',
                                        'price': 120},
                                       {'card_id': 5,
                                        'image': '/static/%D0%B1%D1%83%D0%BB%D0%BE%D1%87%D0%BA%D0%B0%20%D1%81%20%D1%8F%D0%B1%D0%BB%D0%BE%D0%BA%D0%BE%D0%BC.jpeg',
                                        'name': 'булочка с яблоком',
                                        'price': 300},
                                       {'card_id': 6,
                                        'image': '/static/%D0%B1%D1%83%D1%82%D0%B5%D1%80.jpeg',
                                        'name': 'бутер',
                                        'price': 140},
                                       {'card_id': 7,
                                        'image': '/static/%D0%BF%D0%B8%D1%80%D0%BE%D0%B6%D0%BE%D0%BA%20%D1%81%20%D0%BC%D1%8F%D1%81%D0%BE%D0%BC.jpeg',
                                        'name': 'пирожок с мясом',
                                        'price': 120},
                                       {'card_id': 8,
                                        'image': '/static/%D1%81%D0%B0%D0%BC%D1%81%D0%B0.jpeg',
                                        'name': 'самса',
                                        'price': 180},
                                       {'card_id': 9,
                                        'image': '/static/%D1%81%D1%8B%D1%80%D0%BD%D0%B8%D0%BA.jpeg',
                                        'name': 'сырник',
                                        'price': 100},
                                       {'card_id': 10, 'image': '/static/shrek.jpg', 'name': 'шаурма', 'price': 70}]

    # Не понятно, как сохранять картинки в локальном хранилище пайтест. Какой в этом смысл,
    # я не смогу отправить картинку на ручку, валидатор не пропустит, лучше тогда просто из базы
    # вытаскивать названия картинок, как будто это они и есть.
    @pytest.mark.skip
    def test_restaurant_cards_post(self, client):
        file_path = '/home/t1/PycharmProjects/Bakery/backend/application/static/' + 'блины с мясом.jpeg'
        #
        with open(file_path, 'rb') as img1:
            imgStringIO1 = io.BytesIO(img1.read())

        response = client.post('/restaurant/cards', content_type='multipart/form-data',
                               data={'name': 'блины с мясом',
                                     'price': 120,
                                     'image': (imgStringIO1, 'блины с мясом.jpeg')})

        assert response.status_code == 500
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    # здесь не понятно как менять картинку
    @pytest.mark.skip
    def test_restaurant_cards_patch(self, client):
        response = client.patch('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    @pytest.mark.skip
    def test_restaurant_cards_delete(self, client):
        response = client.delete('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    # падают тесты, потому что команду заполнения базы надо редактировать, list_index_error
    # 'date': response[0]['date'],

    def test_restaurant_orders_get(self, client):
        response = client.get('/restaurant/current_orders')

        assert response.status_code == 200
        response = response.get_json()

        assert response == [{'address': '',
                             'amount': '1, 1, 1',
                             'date': response[0]['date'],
                             'name': 'булочка с изюмом, булочка с изюмом, булочка с изюмом',
                             'order_id': 10,
                             'text': ''},
                            {'address': '',
                             'amount': '1, 1, 1',
                             'date': response[1]['date'],
                             'name': 'булочка с вишней, булочка с вишней, булочка с вишней',
                             'order_id': 9,
                             'text': ''},
                            {'address': '',
                             'amount': '1, 1, 1',
                             'date': response[2]['date'],
                             'name': 'пирожок с мясом, пирожок с мясом, пирожок с мясом',
                             'order_id': 7,
                             'text': ''},
                            {'address': 'Белгородская область, город Воскресенск, ул. Славы, 07',
                             'amount': '1, 1, 1',
                             'date': response[3]['date'],
                             'name': 'блины с мясом, блины с мясом, блины с мясом',
                             'order_id': 1,
                             'text': 'Сложно сказать, почему независимые государства будут в равной '
                                     'степени предоставлены сами себе.'},
                            {'address': 'Челябинская область, город Кетозник, наб. Котлетова, 26',
                             'amount': '5, 5, 5',
                             'date': response[4]['date'],
                             'name': 'булочка с яблоком, булочка с яблоком, булочка с яблоком',
                             'order_id': 5,
                             'text': ''},
                            {'address': 'Ленинградская область, город Орехово-Зуево, бульвар '
                                        'Бухарестская, 48',
                             'amount': '4, 4, 4',
                             'date': response[5]['date'],
                             'name': 'булочка с клубникой, булочка с клубникой, булочка с клубникой',
                             'order_id': 4,
                             'text': ''},
                            {'address': 'Ярославская область, город Дорохово, проезд Гагарина, 76',
                             'amount': '3, 3, 3',
                             'date': response[6]['date'],
                             'name': 'булочка с вишней, булочка с вишней, булочка с вишней',
                             'order_id': 2,
                             'text': ''},
                            {'address': 'Омская область, город Щекино, пр. Каршеринга, 16',
                             'amount': '6, 6, 6',
                             'date': response[7]['date'],
                             'name': 'бутер, бутер, бутер',
                             'order_id': 6,
                             'text': ''}]

    @pytest.mark.skip
    def test_restaurant_orders_patch(self, client):
        response = client.patch('/restaurant/orders')

        assert response.status_code == 200
        assert response.get_json() == []

    def test_auth_logout(self, client):
        response = client.get('/auth/logout')

# надо добавить 4 карточки, проверить, что они добавились, одну удалить, проверить, что удалилась,
# и с 3 оставшимися уже работать в баскете и остальных роутах
