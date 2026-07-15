from backend.project.users.models import (
    UserField,
)


class UserFieldService:

    @classmethod
    def get_fields(
        cls,
    ):
        return (

            UserField.objects

            .all()

            .order_by(
                "id",
            )

        )