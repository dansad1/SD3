# =========================================================
# backend/dynamic/field_types/number.py
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import BaseFieldType
from backend.engine.fields.types.registry import register_field_type


@register_field_type
class NumberFieldType(BaseFieldType):

    code = "number"

    label = "Number"

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

        try:

            if field.is_multiple:

                return [
                    float(v)
                    for v in value
                ]

            return float(value)

        except Exception:

            raise ValidationError(
                "Некорректное число"
            )