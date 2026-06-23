from rest_framework.test import APITestCase

from backend.project.users.models import User


class TestMassAssignment(APITestCase):

    def test_cannot_escalate_privileges(self):

        admin = User.objects.get(
            login="root"
        )

        self.client.force_authenticate(
            admin
        )

        payload = {

            "login":
                "evil",

            "password":
                "12345",

            "is_superuser":
                True,

            "is_staff":
                True,

        }

        response = self.client.post(

            "/api/entity/user/create/",

            payload,

            format="json",

        )

        user = User.objects.get(

            login="evil"

        )

        assert (

            user.is_superuser

            is False

        )

        assert (

            user.is_staff

            is False

        )