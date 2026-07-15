from django.core.exceptions import (
    ValidationError,
)


class UserDeleteService:

    @classmethod
    def validate(
        cls,
        actor,
        target,
    ):

        if actor.pk == target.pk:

            raise ValidationError(

                {
                    "detail": [

                        "You cannot delete yourself",

                    ]
                }

            )