# =========================================================
# backend/engine/fields/types/email.py
# =========================================================

import re

from django.core.validators import (
    validate_email,
)

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.string import (
    StringFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


# =====================================================
# CONSTANTS
# =====================================================

MAX_EMAIL_LENGTH = 254

LOCAL_MAX_LENGTH = 64

DOMAIN_MAX_LENGTH = 253

# =====================================================
# REGEX
# =====================================================

EMAIL_RE = re.compile(

    r"^[^\s@]+@[^\s@]+\.[^\s@]+$",

    re.IGNORECASE,
)


@register_field_type
class EmailFieldType(
    StringFieldType
):

    code = "email"

    label = "Email"

    widget = "email"

    searchable = True

    sortable = True

    filterable = True

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_email_value(
        self,
        value,
    ):

        value = value.lower()

        if len(value) > MAX_EMAIL_LENGTH:

            raise ValidationError(
                "Email слишком длинный"
            )

        try:

            local,
            domain = value.rsplit(
                "@",
                1,
            )

        except ValueError:

            raise ValidationError(
                "Некорректный email"
            )

        if (
            len(local)
            > LOCAL_MAX_LENGTH
        ):

            raise ValidationError(
                "Слишком длинная локальная часть email"
            )

        if (
            len(domain)
            > DOMAIN_MAX_LENGTH
        ):

            raise ValidationError(
                "Слишком длинный домен"
            )

        if not EMAIL_RE.match(
            value
        ):

            raise ValidationError(
                "Некорректный email"
            )

        try:

            validate_email(
                value
            )

        except Exception:

            raise ValidationError(
                "Некорректный email"
            )

        return value

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        value = super().validate(
            field,
            value,
        )

        if value in (
            None,
            "",
        ):

            return value

        if field.is_multiple:

            return [
                self.validate_email_value(v)
                for v in value
            ]

        return self.validate_email_value(
            value
        )

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):

        value = super().normalize(
            field,
            value,
        )

        if value is None:

            return None

        if field.is_multiple:

            return [
                str(v).lower()
                for v in value
            ]

        return str(
            value
        ).lower()

    # =====================================================
    # UI
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "autocomplete":
                "email",

            "maxLength":
                MAX_EMAIL_LENGTH,
        })

        return schema