# =========================================================
# backend/dynamic/field_types/date.py
# =========================================================

from datetime import date

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import BaseFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class DateFieldType(BaseFieldType):

    code = "date"

    label = "Date"

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

        if isinstance(
            value,
            date,
        ):
            return value

        try:

            return date.fromisoformat(
                str(value)
            )

        except Exception:

            raise ValidationError(
                "Некорректная дата"
            )

    def serialize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        return value.isoformat()

    def deserialize(
        self,
        field,
        value,
    ):

        if not value:
            return None

        return date.fromisoformat(
            str(value)
        )

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "date"
        )