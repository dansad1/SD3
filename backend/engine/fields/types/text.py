from backend.engine.fields.types.registry import (
    register_field_type,
)

from backend.engine.fields.types.string import (
    StringFieldType,
)


@register_field_type
class TextFieldType(StringFieldType):

    code = "text"

    label = "Text"

    widget = "textarea"

    DEFAULT_MAX_LENGTH = 50000

    ABSOLUTE_MAX_LENGTH = 100000

    sortable = False

    searchable = True

    filterable = False

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

            "multiline":
                True,

            "rows":
                6,
        })

        return schema