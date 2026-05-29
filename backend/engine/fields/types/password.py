from rest_framework.exceptions import ValidationError

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
            return

        obj.set_password(
            value
        )


@register_field_type
class PasswordFieldType(
    BaseFieldType
):

    code = "password"

    label = "Password"

    serializeable = False

    searchable = False

    filterable = False

    accessor = PasswordAccessor()

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

        })

        return schema

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

        return value

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

    def serialize(
        self,
        field,
        value,
    ):
        return None