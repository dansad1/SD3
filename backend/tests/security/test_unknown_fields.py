from rest_framework.test import APITestCase


class TestUnknownFields(APITestCase):

    def test_unknown_payload(self):

        response = self.client.post(

            "/api/entity/user/create/",

            {

                "abracadabra":

                    123

            },

            format="json",

        )

        assert (

            response.status_code

            != 500

        )