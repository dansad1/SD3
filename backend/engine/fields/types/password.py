from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)

import re


# =========================================================
# ACCESSOR
# =========================================================

class PasswordAccessor:

    # =====================================================
    # READ
    # =====================================================

    def get(
        self,
        obj,
        field,
    ):

        """
        Никогда не возвращаем hash.
        """

        return None

    # =====================================================
    # WRITE
    # =====================================================

    def set(
        self,
        obj,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return

        obj.set_password(
            value
        )


# =========================================================
# FIELD TYPE
# =========================================================

@register_field_type
class PasswordFieldType(BaseFieldType):

    code = "password"

    label = "Password"

    # =====================================================
    # SECURITY
    # =====================================================

    serializeable = False

    searchable = False

    filterable = False

    accessor = PasswordAccessor()

    # =====================================================
    # LIMITS
    # =====================================================

    MIN_LENGTH = 8

    MAX_LENGTH = 128

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

            "inputType":
                "password",

            "autocomplete":
                "new-password",

            "minLength":
                self.MIN_LENGTH,

            "maxLength":
                self.MAX_LENGTH,
        })

        return schema

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

        # =============================================
        # EMPTY
        # =============================================

        if value in (
            None,
            "",
        ):
            return value

        # =============================================
        # TYPE
        # =============================================

        if not isinstance(
            value,
            str,
        ):

            raise ValidationError(
                "Некорректный пароль"
            )

        # =============================================
        # TRIM
        # =============================================

        value = value.strip()

        # =============================================
        # LENGTH
        # =============================================

        if len(value) < self.MIN_LENGTH:

            raise ValidationError(
                f"Минимум {self.MIN_LENGTH} символов"
            )

        if len(value) > self.MAX_LENGTH:

            raise ValidationError(
                "Пароль слишком длинный"
            )

        # =============================================
        # CONTROL CHARS
        # =============================================

        if any(
            ord(c) < 32
            for c in value
        ):

            raise ValidationError(
                "Пароль содержит недопустимые символы"
            )

        # =============================================
        # COMMON PASSWORDS
        # =============================================

        common = {

            "password",
            "12345678",
            "qwerty",
            "admin",
            "123123123",
            "11111111",
            "password123",
        }

        if value.lower() in common:

            raise ValidationError(
                "Слишком простой пароль"
            )

        # =============================================
        # COMPLEXITY
        # =============================================

        checks = [

            re.search(r"[A-Z]", value),

            re.search(r"[a-z]", value),

            re.search(r"\d", value),
        ]

        passed = sum(
            bool(x)
            for x in checks
        )

        if passed < 2:

            raise ValidationError(
                "Используйте буквы и цифры"
            )

        # =============================================
        # SPACES ONLY
        # =============================================

        if not value.strip():

            raise ValidationError(
                "Некорректный пароль"
            )

        return value

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return None

        return str(value)

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):

        """
        Никогда не сериализуем password/hash.
        """

        return None