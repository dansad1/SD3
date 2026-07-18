from django.core.exceptions import (
    ValidationError,
)


class UserRoleValidationService:

    RESERVED_CODES = {
        "root",
        "system",
        "superadmin",
    }

    @classmethod
    def validate(
        cls,
        payload,
        instance=None,
    ):
        errors = {}

        cls.validate_code(
            payload=payload,
            errors=errors,
        )



        if errors:
            raise ValidationError(
                errors,
            )

        return payload

    # =====================================================
    # CODE
    # =====================================================

    @classmethod
    def validate_code(
        cls,
        payload,
        errors,
    ):
        code = payload.get(
            "code",
        )

        if not code:
            return

        if (
            code.lower()
            in cls.RESERVED_CODES
        ):
            errors["code"] = [
                "Reserved role code",
            ]


