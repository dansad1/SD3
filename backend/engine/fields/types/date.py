from datetime import (
    date,
    datetime,
)

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
class DateFieldType(BaseFieldType):

    code = "date"

    label = "Date"

    widget = "date"

    sortable = True

    searchable = False

    filterable = True

    MIN_DATE = date(
        1900,
        1,
        1,
    )

    MAX_DATE = date(
        2100,
        12,
        31,
    )

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_date(
        self,
        value,
    ):

        if isinstance(
            value,
            date,
        ) and not isinstance(
            value,
            datetime,
        ):
            return value

        if isinstance(
            value,
            datetime,
        ):
            return value.date()

        if not isinstance(
            value,
            (
                str,
                int,
                float,
            ),
        ):
            raise ValidationError(
                "Некорректная дата"
            )

        raw = str(value).strip()

        if not raw:
            raise ValidationError(
                "Некорректная дата"
            )

        try:
            return date.fromisoformat(
                raw
            )

        except Exception:
            raise ValidationError(
                "Некорректная дата"
            )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_date(
        self,
        value,
    ):

        parsed = self.to_date(
            value
        )

        if parsed < self.MIN_DATE:
            raise ValidationError(
                "Дата слишком маленькая"
            )

        if parsed > self.MAX_DATE:
            raise ValidationError(
                "Дата слишком большая"
            )

        return parsed

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
                self.validate_date(v)
                for v in value
            ]

        return self.validate_date(
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
                self.validate_date(v)
                for v in value
            ]

        return self.validate_date(
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

        if isinstance(
            value,
            datetime,
        ):
            value = value.date()

        return value.isoformat()

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        if not value:
            return None

        return self.to_date(
            value
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

        schema.update({

            "min":
                self.MIN_DATE.isoformat(),

            "max":
                self.MAX_DATE.isoformat(),
        })

        return schema