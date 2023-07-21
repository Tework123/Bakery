import pytest


@pytest.mark.usefixtures('client', 'add_data_to_db')
class TestProfile:

    def test_main(self, client):
        response = client.get('/profile/pass_orders')

        assert response.status_code == 200
        # assert response.get_json() == {'expected_error_description'}
