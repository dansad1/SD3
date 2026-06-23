from rest_framework.test import APITestCase


class TestIDOR(APITestCase):

    def test_cannot_edit_company(self):

        self.client.force_authenticate(

            self.operator

        )

        response = self.client.patch(

            "/api/entity/company/1/",

            {

                "name":

                    "Hacked"

            },

            format="json",

        )

        assert (

            response.status_code

            == 403

        )