import pytest


@pytest.mark.usefixtures('client')
class TestRegisterErrors:

    @pytest.mark.parametrize('test_input, expected_error_description, expected_status_code',
                             [({'name': 'grisha',
                                'email': 'pasf@mailru',
                                'password': '12345'}, 'email некорректен', 400),
                              ({'name': 'grisha',
                                'email': 'pasf@mail.ru',
                                'password': '1s45'}, 'пароль должен содержать...', 400)
                              ])
    def test_register_app(self, client, test_input, expected_error_description, expected_status_code):
        response = client.post('main/register', json=test_input)

        assert response.status_code == expected_status_code
        assert response.get_json() == expected_error_description

# сделать адекватно, также надо добавить аутентификацию с jwt токеном, по другому никак
