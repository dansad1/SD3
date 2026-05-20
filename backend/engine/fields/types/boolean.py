# =========================================================
# backend/dynamic/field_types/boolean.py
# =========================================================
from backend.engine.fields.types.base import BaseFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class BooleanFieldType(BaseFieldType):

    code = "boolean"

    label = "Boolean"

    TRUE_VALUES = {
        True,
        1,
        "1",
        "true",
        "True",
        "yes",
        "on",
    }

    FALSE_VALUES = {
        False,
        0,
        "0",
        "false",
        "False",
        "no",
        "off",
    }

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

        if field.is_multiple:

            return [
                self.normalize_single(v)
                for v in value
            ]

        return self.normalize_single(
            value
        )

    def normalize_single(
        self,
        value,
    ):

        if value in self.TRUE_VALUES:
            return True

        if value in self.FALSE_VALUES:
            return False

        return bool(value)

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "checkbox"
        )