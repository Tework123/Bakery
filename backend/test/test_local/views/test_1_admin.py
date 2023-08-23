import pytest


@pytest.mark.usefixtures('client', 'add_test_data_to_db')
class TestAdminUnauthorized:

    @pytest.mark.parametrize('test_input, expected_error_description, expected_status_code',
                             [(
                                     {"email": "restaurant1@mail.ru"}, {'data': 'Вы не зашли в аккаунт'}, 401)
                             ])
    def test_create_admin_post(self, client, test_input, expected_error_description, expected_status_code):
        response = client.post('/admin/create_restaurant', json=test_input)

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_create_admin_get(self, client):
        response = client.get('/admin/create_restaurant')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}

    def test_site_statistics_get(self, client):
        response = client.get('/admin/site_statistics')

        assert response.status_code == 401
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}


@pytest.mark.usefixtures('client')
class TestAdminAuthorized:
    # может быть оставить тестового админа, но сделать ему сложный емайл и также авторизацию по коду
    # в тестах можно это сделать, вместе с кодом отправлять, хотя код на почту улетает...
    # надо реально оставить вход без пароля, но нужны сложные емайлы
    def test_auth_admin(self, client):
        response = client.post('/auth/login', json={"email": "adcde@mail.ru"})

        assert response.status_code == 200
        assert response.get_json() == {"data": "Вход тестового главного админа выполнен успешно"}

    @pytest.mark.parametrize('test_input, expected_error_description, expected_status_code',
                             [(
                                     {"email": "restaurant1@mail.ru"}, {'data': 'Работник пекарни создан успешно'},
                                     200),
                                 ({
                                      'email': 'restaurant1mail.ru',
                                  }, {'message': 'Email записан некорректно'}, 400)
                             ])
    def test_create_admin_post(self, client, test_input, expected_error_description, expected_status_code):
        response = client.post('/admin/create_restaurant', json=test_input)

        assert response.status_code == expected_status_code
        assert response.get_json() == expected_error_description

    def test_create_admin_get(self, client):
        response = client.get('/admin/create_restaurant')

        assert response.status_code == 200
        assert response.get_json() == [{'email': 'restaurant1@mail.ru', 'role': 'restaurant', 'user_id': 7}]

    def test_site_statistics_get(self, client):
        response = client.get('/admin/site_statistics')

        assert response.status_code == 200
        assert response.get_json() == {'data': 'some statistics'}

    def test_auth_logout(self, client):
        response = client.get('/auth/logout')
