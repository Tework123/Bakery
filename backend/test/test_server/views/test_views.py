import pytest
import requests


@pytest.mark.usefixtures('url_for_test')
class TestRegisterErrors:

    @pytest.mark.parametrize('test_input, expected_error_description, expected_status_code',
                             [({'name': 'grisha',
                                'email': 'pasf@mailru',
                                'password': '12345'}, 'email некорректен', 400),
                              ({'name': 'grisha',
                                'email': 'pasf@mail.ru',
                                'password': '1s45'}, 'пароль должен содержать...', 400)
                              ])
    def test_register_app(self, url_for_test, test_input, expected_error_description, expected_status_code):
        response = requests.post(url_for_test + 'main/register', json=test_input)

        assert response.status_code == expected_status_code
        assert response.json() == expected_error_description

# сделать адекватно, также надо добавить аутентификацию с jwt токеном, здесь тесты будут немного другие
