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
    searchable = True
    filterable = True

    features = [
        "required",
        "placeholder",
        "help_text",
    ]

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_date(
        self,
        value,
    ):

        if (
            isinstance(
                value,
                date,
            )
            and not isinstance(
                value,
                datetime,
            )
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
        return self.to_date(
            value
        )

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

        return (
            self.to_date(value)
            .isoformat()
        )

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

        return queryset.filter(
            **{
                field.name:
                    self.to_date(
                        value
                    )
            }
        )