from backend.engine.fields.types.registry import (
    register_field_type,
)

from backend.engine.fields.types.string import (
    StringFieldType,
)


@register_field_type
class TextFieldType(
    StringFieldType
):

    code = "text"

    label = "Text"

    widget = "textarea"

    sortable = True
    searchable = True
    filterable = True

    features = [
        "required",
        "placeholder",
        "help_text",
    ]

    DEFAULT_ROWS = 6

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "multiline": True,

            "rows":
                self.DEFAULT_ROWS,

        })

        return schema