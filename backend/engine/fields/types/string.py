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

    widget = "text"

    searchable = True

    sortable = True

    filterable = True

    # =====================================================
    # LIMITS
    # =====================================================

    DEFAULT_MAX_LENGTH = 255

    ABSOLUTE_MAX_LENGTH = 10000

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_string(
        self,
        value,
    ):

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

        value = unicodedata.normalize(
            "NFKC",
            value,
        )

        return value.strip()

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_string(
        self,
        field,
        value,
    ):

        value = self.to_string(
            value
        )

        # =============================================
        # LENGTH
        # =============================================

        max_length = (
            field.max_value
            or self.DEFAULT_MAX_LENGTH
        )

        try:

            max_length = int(
                max_length
            )

        except (
            TypeError,
            ValueError,
        ):

            max_length = (
                self.DEFAULT_MAX_LENGTH
            )

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

            if (
                ord(char) < 32
                and char not in (
                    "\n",
                    "\r",
                    "\t",
                )
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

        if value in (
            None,
            "",
        ):

            return value

        if field.is_multiple:

            return [

                self.validate_string(
                    field,
                    item,
                )

                for item in value
            ]

        return self.validate_string(
            field,
            value,
        )

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
                self.to_string(v)
                for v in value
            ]

        return self.to_string(
            value
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

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "maxLength":

                field.max_value

                or self.DEFAULT_MAX_LENGTH,

            "multiline":
                False,
        })

        return schema