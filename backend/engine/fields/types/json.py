# =========================================================
# backend/dynamic/field_types/json_type.py
# =========================================================
from backend.engine.fields.types.base import BaseFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class JSONFieldType(BaseFieldType):

    code = "json"

    label = "JSON"

    def normalize(
        self,
        field,
        value,
    ):

        return value

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "json"
        )