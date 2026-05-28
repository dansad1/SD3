# backend/engine/fields/types/email.py

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

# =====================================================
# FIELD TYPE
# =====================================================

class EmailFieldType(StringFieldType):

    code = "email"

    label = "Email"

    searchable = True

    # =================================================
    # VALIDATE
    # =================================================

    def validate(
        self,
        field,
        value,
    ):

        value = super().validate(
            field,
            value,
        )

        # =============================================
        # EMPTY
        # =============================================

        if not value:

            return value

        # =============================================
        # TYPE
        # =============================================

        if not isinstance(
            value,
            str,
        ):

            raise ValidationError(
                "Некорректный email"
            )

        # =============================================
        # NORMALIZE
        # =============================================

        value = (
            value
            .strip()
            .lower()
        )

        # =============================================
        # LENGTH
        # =============================================

        if len(value) > MAX_EMAIL_LENGTH:

            raise ValidationError(
                "Email слишком длинный"
            )

        # =============================================
        # BASIC FORMAT
        # =============================================

        if not EMAIL_RE.match(value):

            raise ValidationError(
                "Введите корректный email"
            )

        # =============================================
        # SPLIT
        # =============================================

        try:

            local,
            domain = value.rsplit(
                "@",
                1,
            )

        except ValueError:

            raise ValidationError(
                "Введите корректный email"
            )

        # =============================================
        # LOCAL LENGTH
        # =============================================

        if len(local) > LOCAL_MAX_LENGTH:

            raise ValidationError(
                "Некорректный email"
            )

        # =============================================
        # DOMAIN LENGTH
        # =============================================

        if len(domain) > DOMAIN_MAX_LENGTH:

            raise ValidationError(
                "Некорректный email"
            )

        # =============================================
        # DOT CHECKS
        # =============================================

        if ".." in value:

            raise ValidationError(
                "Некорректный email"
            )

        if domain.startswith("."):

            raise ValidationError(
                "Некорректный email"
            )

        if domain.endswith("."):

            raise ValidationError(
                "Некорректный email"
            )

        # =============================================
        # DJANGO VALIDATOR
        # =============================================

        try:

            validate_email(value)

        except ValidationError:

            raise ValidationError(
                "Введите корректный email"
            )

        return value

    # =================================================
    # NORMALIZE
    # =================================================

    def normalize(
        self,
        field,
        value,
    ):

        if not value:

            return value

        return (
            str(value)
            .strip()
            .lower()
        )