import pytest


@pytest.mark.usefixtures('client')
class TestAuth:

    @pytest.mark.parametrize('test_input, expected_error_description, expected_status_code',
                             [({'email': 'pasf@mail.ru'},
                               {'data': 'Для подтверждения регистрации введите код из почты'}, 200),
                              ({"email": "user@mail.ru"},
                               {'data': 'Вход тестового пользователя выполнен успешно'}, 200),
                              ({'email': 'pasf@mail.ru'},
                               {'data': 'Вы уже вошли в аккаунт'}, 200)
                              ])
    def test_auth(self, client, test_input, expected_error_description, expected_status_code):
        response = client.post('/auth/login', json=test_input)

        assert response.status_code == expected_status_code
        assert response.get_json() == expected_error_description

    def test_auth_logout(self, client):
        response = client.get('/auth/logout')

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Вы вышли из аккаунта'}

    def test_auth_logout_not_login(self, client):
        response = client.get('/auth/logout')

        assert response.status_code == 200
        assert response.get_json() == {'data': 'Вы не зашли в аккаунт'}
