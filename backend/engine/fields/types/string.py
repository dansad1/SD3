# =========================================================
# backend/engine/fields/types/string.py
# =========================================================

import re
import unicodedata

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

    searchable = True

    sortable = True

    filterable = True

    # =====================================================
    # LIMITS
    # =====================================================

    DEFAULT_MAX_LENGTH = 255

    ABSOLUTE_MAX_LENGTH = 10000

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        value = super().validate(
            field,
            value,
        )

        # =============================================
        # EMPTY
        # =============================================

        if value in (
            None,
            "",
        ):

            return value

        # =============================================
        # MULTIPLE
        # =============================================

        values = (
            value
            if field.is_multiple
            else [value]
        )

        validated = []

        for item in values:

            validated.append(
                self.validate_single(
                    field,
                    item,
                )
            )

        if field.is_multiple:

            return validated

        return validated[0]

    # =====================================================
    # VALIDATE SINGLE
    # =====================================================

    def validate_single(
        self,
        field,
        value,
    ):

        # =============================================
        # TYPE
        # =============================================

        if not isinstance(
            value,
            (
                str,
                int,
                float,
            ),
        ):

            raise ValidationError(
                "Некорректное значение"
            )

        value = str(value)

        # =============================================
        # UNICODE NORMALIZATION
        # =============================================

        value = unicodedata.normalize(
            "NFKC",
            value,
        )

        # =============================================
        # TRIM
        # =============================================

        value = value.strip()

        # =============================================
        # LENGTH
        # =============================================

        max_length = getattr(
            field,
            "max_length",
            None,
        ) or self.DEFAULT_MAX_LENGTH

        max_length = min(
            max_length,
            self.ABSOLUTE_MAX_LENGTH,
        )

        if len(value) > max_length:

            raise ValidationError(
                f"Максимум {max_length} символов"
            )

        # =============================================
        # CONTROL CHARS
        # =============================================

        for char in value:

            if ord(char) < 32:

                if char not in (
                    "\n",
                    "\r",
                    "\t",
                ):

                    raise ValidationError(
                        "Недопустимые символы"
                    )

        # =============================================
        # REGEX
        # =============================================

        if field.regex:

            try:

                matched = re.fullmatch(
                    field.regex,
                    value,
                )

            except re.error:

                raise ValidationError(
                    "Некорректная regex-конфигурация"
                )

            if not matched:

                raise ValidationError(
                    "Некорректный формат"
                )

        return value

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

        value = unicodedata.normalize(
            "NFKC",
            str(value),
        )

        return value.strip()

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

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "maxLength":

                getattr(
                    field,
                    "max_length",
                    None,
                )

                or self.DEFAULT_MAX_LENGTH,

            "multiline":
                False,
        })

        return schema