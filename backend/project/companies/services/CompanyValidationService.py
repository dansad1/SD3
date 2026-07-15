from django.core.exceptions import (
    ValidationError,
)


class CompanyValidationService:

    @classmethod
    def validate(
        cls,
        payload,
    ):

        errors = {}

        if not payload.get(
            "name",
        ):

            errors["name"] = [
                "Название обязательно",
            ]

        if errors:

            raise ValidationError(
                errors,
            )