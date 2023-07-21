import pytest


@pytest.mark.usefixtures('client')
class TestRestaurantUnauthorized:

    def test_restaurant_cards_get(self, client):
        response = client.get('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_cards_post(self, client):
        response = client.get('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_cards_patch(self, client):
        response = client.get('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_cards_delete(self, client):
        response = client.get('/restaurant/cards')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_orders_get(self, client):
        response = client.get('/restaurant/orders')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_restaurant_orders_patch(self, client):
        response = client.get('/restaurant/orders')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

# надо добавить 4 карточки, проверить, что они добавились, одну удалить, проверить, что удалилась,
# и с 3 оставшимися уже работать в баскете и остальных роутах
