# =========================================================
# backend/dynamic/field_types/datetime.py
# =========================================================

from datetime import datetime

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import BaseFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class DateTimeFieldType(BaseFieldType):

    code = "datetime"

    label = "DateTime"

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
            datetime,
        ):
            return value

        try:

            return datetime.fromisoformat(
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

        return value.strftime(
            "%Y-%m-%dT%H:%M"
        )
    def deserialize(
        self,
        field,
        value,
    ):

        if not value:
            return None

        return datetime.fromisoformat(
            str(value)
        )

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "datetime"
        )