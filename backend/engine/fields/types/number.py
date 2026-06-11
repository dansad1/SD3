# =========================================================
# backend/dynamic/field_types/number.py
# =========================================================

import math

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
class NumberFieldType(BaseFieldType):

    code = "number"

    label = "Number"

    widget = "number"

    sortable = True
    searchable = False
    filterable = True

    features = [
        "default_value",
        "required",
        "unique",
        "min_value",
        "max_value",
        "placeholder",
        "help_text",
    ]

    default_value_widget = "number"

    # =====================================================
    # LIMITS
    # =====================================================

    MAX_ABS = 10 ** 15

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_number(
        self,
        value,
    ):

        if isinstance(
            value,
            bool,
        ):
            raise ValidationError(
                "Некорректное число"
            )

        try:

            number = float(
                value
            )

        except Exception:

            raise ValidationError(
                "Некорректное число"
            )

        if not math.isfinite(
            number
        ):
            raise ValidationError(
                "Некорректное число"
            )

        if abs(number) > self.MAX_ABS:
            raise ValidationError(
                "Слишком большое число"
            )

        return number

    # =====================================================
    # FIELD LIMITS
    # =====================================================

    def get_min_number(
        self,
        field,
    ):

        if field.min_value in (
            None,
            "",
        ):
            return None

        return self.to_number(
            field.min_value
        )

    def get_max_number(
        self,
        field,
    ):

        if field.max_value in (
            None,
            "",
        ):
            return None

        return self.to_number(
            field.max_value
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_number(
        self,
        field,
        value,
    ):

        number = self.to_number(
            value
        )

        min_value = (
            self.get_min_number(
                field
            )
        )

        max_value = (
            self.get_max_number(
                field
            )
        )

        if (
            min_value is not None
            and number < min_value
        ):
            raise ValidationError(
                f"Минимальное значение: {min_value}"
            )

        if (
            max_value is not None
            and number > max_value
        ):
            raise ValidationError(
                f"Максимальное значение: {max_value}"
            )

        return number

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
                self.validate_number(
                    field,
                    v,
                )
                for v in value
            ]

        return self.validate_number(
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

        if value in (
            None,
            "",
        ):
            return None

        if field.is_multiple:

            return [
                self.validate_number(
                    field,
                    v,
                )
                for v in value
            ]

        return self.validate_number(
            field,
            value,
        )

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        return value

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return None

        return self.to_number(
            value
        )

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return queryset

        try:

            value = self.to_number(
                value
            )

        except ValidationError:

            return queryset.none()

        return queryset.filter(
            **{
                field.name:
                    value
            }
        )

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

        min_value = (
            self.get_min_number(
                field
            )
        )

        max_value = (
            self.get_max_number(
                field
            )
        )

        schema.update({

            "inputType":
                "number",

        })

        if min_value is not None:

            schema["min"] = (
                min_value
            )

        if max_value is not None:

            schema["max"] = (
                max_value
            )

        return schema