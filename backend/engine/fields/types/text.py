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

    sortable = False
    searchable = True
    filterable = False

    features = [
        "default_value",
        "required",
        "max_value",
        "placeholder",
        "help_text",
    ]

    default_value_widget = "textarea"

    DEFAULT_MAX_LENGTH = 50000

    ABSOLUTE_MAX_LENGTH = 100000

    DEFAULT_ROWS = 6

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
                "textarea",

            "multiline":
                True,

            "rows":
                self.DEFAULT_ROWS,

        })

        return schema