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
    searchable = True
    filterable = True

    features = [
        "required",
        "unique",
        "placeholder",
        "help_text",
    ]

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

        if (
            abs(number)
            > self.MAX_ABS
        ):
            raise ValidationError(
                "Слишком большое число"
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
                self.to_number(v)
                for v in value
            ]

        return self.to_number(
            value
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
                self.to_number(v)
                for v in value
            ]

        return self.to_number(
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