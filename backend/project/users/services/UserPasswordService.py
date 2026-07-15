from django.contrib.auth.password_validation import (
    validate_password,
)
from django.core.exceptions import (
    ValidationError,
)


class UserPasswordService:

    MASK = "********"

    # =====================================================
    # VALIDATION
    # =====================================================

    @classmethod
    def validate(
        cls,
        payload,
        instance=None,
    ):

        errors = {}

        password = payload.get(
            "password",
        )

        if (
            instance is None
            and not password
        ):

            errors["password"] = [
                "Password required",
            ]

        if password not in (
            None,
            "",
            cls.MASK,
        ):

            try:

                validate_password(
                    password,
                    user=instance,
                )

            except ValidationError as exc:

                errors["password"] = list(
                    exc.messages,
                )

        if errors:

            raise ValidationError(
                errors,
            )

    # =====================================================
    # APPLY
    # =====================================================

    @classmethod
    def apply(
        cls,
        instance,
        payload,
    ):

        password = payload.pop(
            "password",
            None,
        )

        if password in (
            None,
            "",
            cls.MASK,
        ):
            return

        instance.set_password(
            password,
        )