# =========================================================
# backend/engine/fields/types/string.py
# =========================================================

import re

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class StringFieldType(BaseFieldType):

    code = "string"

    label = "String"

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        if field.is_multiple:

            return [
                str(v)
                for v in value
            ]

        return str(value)

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        super().validate(
            field,
            value,
        )

        if value in (
            None,
            "",
        ):
            return

        values = (
            value
            if field.is_multiple
            else [value]
        )

        if field.regex:

            for item in values:

                if not re.match(
                    field.regex,
                    str(item),
                ):

                    raise ValidationError(
                        "Некорректный формат"
                    )

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        if field.is_multiple:

            return [
                str(v)
                for v in value
            ]

        return str(value)

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        if field.is_multiple:

            return [
                str(v)
                for v in value
            ]

        return str(value)

    # =====================================================
    # UI
    # =====================================================

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "TextInput"
        )