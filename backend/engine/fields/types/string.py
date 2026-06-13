import unicodedata

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class StringFieldType(
    BaseFieldType
):

    code = "string"

    label = "String"

    widget = "text"

    searchable = True
    sortable = True
    filterable = True

    features = [
        "required",
        "unique",
        "placeholder",
        "help_text",
    ]

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_string(
        self,
        value,
    ):

        if not isinstance(
            value,
            (
                str,
                int,
                float,
            ),
        ):
            raise ValidationError(
                "Некорректное значение"
            )

        value = str(value)

        value = unicodedata.normalize(
            "NFKC",
            value,
        )

        value = value.strip()

        for char in value:

            if (
                ord(char) < 32
                and char not in (
                    "\n",
                    "\r",
                    "\t",
                )
            ):
                raise ValidationError(
                    "Недопустимые символы"
                )

        return value

    # =====================================================
    # VALIDATION
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
                self.to_string(v)
                for v in value
            ]

        return self.to_string(
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

        if value is None:
            return None

        if field.is_multiple:

            return [
                self.to_string(v)
                for v in value
            ]

        return self.to_string(
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

        if value is None:
            return None

        if field.is_multiple:
            return [str(v) for v in value]

        return str(value)

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        if field.is_multiple:
            return [str(v) for v in value]

        return str(value)

    def get_schema(
            self,
            field,
    ):

        schema = super().get_schema(
            field
        )

        if field.choices:
            schema.update({

                "widget": "select",

                "options":
                    field.choices,

            })

        return schema