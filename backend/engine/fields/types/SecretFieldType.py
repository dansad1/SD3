from backend.engine.fields.types.string import (
    StringFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class SecretFieldType(
    StringFieldType,
):
    code = "secret"
    label = "Secret"
    widget = "password"

    searchable = False
    sortable = False
    filterable = False

    features = [
        "required",
        "help_text",
    ]

    MASK = "********"

    def normalize(
        self,
        field,
        value,
    ):
        if value in (
            None,
            "",
            self.MASK,
        ):
            return None

        return str(value)

    def serialize(
        self,
        field,
        value,
    ):
        if value:
            return self.MASK

        return ""

    def should_save(
        self,
        field,
        value,
    ):
        return value not in (
            None,
            "",
            self.MASK,
        )

    def get_schema(
        self,
        field,
    ):
        schema = super().get_schema(
            field
        )

        schema.update({
            "widget": "password",
            "autocomplete": "new-password",
        })

        return schema