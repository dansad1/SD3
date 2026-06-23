from rest_framework.test import APITestCase


class TestScope(APITestCase):

    def test_scope(self):

        response = self.client.get(

            "/api/entity/company/list/"

        )

        assert (

            response.status_code

            == 403

        )