from rest_framework.test import APITestCase


class TestXSS(APITestCase):

    def test_xss_payload(self):

        payload = {

            "name":

                "<img src=x onerror=alert(1)>"

        }

        response = self.client.post(

            "/api/entity/company/create/",

            payload,

            format="json",

        )

        assert (

            response.status_code

            < 500

        )