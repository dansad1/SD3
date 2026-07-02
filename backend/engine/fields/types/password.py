from django.core.exceptions import ValidationError

from backend.engine.fields.types.base import (
    BaseFieldType,
)
from backend.engine.fields.types.registry import (
    register_field_type,
)


class PasswordAccessor:

    MASK = "********"

    def get(
        self,
        obj,
        field,
    ):
        if getattr(obj, "pk", None):
            return self.MASK

        return ""

    def set(
        self,
        obj,
        field,
        value,
    ):
        if value in (
            None,
            "",
            self.MASK,
        ):
            return obj

        obj.set_password(value)

        return obj


@register_field_type
class PasswordFieldType(
    BaseFieldType,
):

    code = "password"

    label = "Password"

    widget = "password"

    searchable = False
    sortable = False
    filterable = False

    accessor = PasswordAccessor()

    features = [
        "required",
        "help_text",
    ]

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
            self.accessor.MASK,
        ):
            return value

        if not isinstance(
            value,
            str,
        ):
            raise ValidationError(
                "Некорректное значение",
            )

        return value.strip()

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
            self.accessor.MASK,
        ):
            return None

        return str(
            value,
        ).strip()

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        return self.accessor.MASK if value else ""

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
            field,
        )

        schema.update({

            "autocomplete":
                "new-password",

            "minLength":
                self.MIN_LENGTH,

            "maxLength":
                self.MAX_LENGTH,

        })

        return schema