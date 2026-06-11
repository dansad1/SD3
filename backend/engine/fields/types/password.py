from rest_framework.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


class PasswordAccessor:

    def get(
        self,
        obj,
        field,
    ):
        return None

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
            return obj

        obj.set_password(
            value
        )

        return obj


@register_field_type
class PasswordFieldType(
    BaseFieldType
):

    code = "password"

    label = "Password"

    widget = "password"

    searchable = False
    filterable = False
    sortable = False

    accessor = PasswordAccessor()

    features = [
        "required",
        "help_text",
    ]

    # =====================================================
    # PASSWORD POLICY
    # =====================================================

    MIN_LENGTH = 8
    MAX_LENGTH = 256

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

        if not isinstance(
            value,
            str,
        ):
            raise ValidationError(
                "Некорректное значение"
            )

        value = value.strip()

        if (
            len(value)
            < self.MIN_LENGTH
        ):
            raise ValidationError(
                f"Минимум {self.MIN_LENGTH} символов"
            )

        if (
            len(value)
            > self.MAX_LENGTH
        ):
            raise ValidationError(
                f"Максимум {self.MAX_LENGTH} символов"
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

        return str(
            value
        )

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        return None

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):
        return None

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

            "reveal":
                False,

        })

        return schema