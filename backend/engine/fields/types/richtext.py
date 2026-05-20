# =========================================================
# backend/dynamic/field_types/richtext.py
# =========================================================
from backend.engine.fields.types.registry import register_field_type
from backend.engine.fields.types.string import StringFieldType


@register_field_type
class RichTextFieldType(StringFieldType):

    code = "richtext"

    label = "RichText"

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "richtext"
        )