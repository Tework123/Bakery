import pytest


@pytest.mark.usefixtures('client', 'add_data_to_db')
class TestMain:

    @pytest.mark.parametrize('test_input, expected_error_description, expected_status_code',
                             [(
                              {"email": "user@mail.ru"}, {'data': 'Вход тестового пользователя выполнен успешно'}, 200),
                              ({
                                   'email': 'pasf@mail.ru',
                               }, {'message': 'Данный email не зарегистрирован'}, 403)
                              ])
    def test_main(self, client, test_input, expected_error_description, expected_status_code):
        response = client.post('/auth/login', json=test_input)

        assert response.status_code == expected_status_code
        assert response.get_json() == expected_error_description

# надо протестить тогда всех тестовых пользователей, а что с данными? они рандомные, хз пока что
# статус проверять как то не очень
