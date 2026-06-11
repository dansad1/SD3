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

    features = [
        "default_value",
        "required",
        "min_value",
        "max_value",
        "placeholder",
        "help_text",
    ]

    default_value_widget = "date"

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

        if isinstance(value, date) and not isinstance(value, datetime):
            return value

        if isinstance(value, datetime):
            return value.date()

        if not isinstance(value, (str, int, float)):
            raise ValidationError(
                "Некорректная дата"
            )

        raw = str(value).strip()

        if not raw:
            raise ValidationError(
                "Некорректная дата"
            )

        try:
            return date.fromisoformat(raw)

        except Exception:
            raise ValidationError(
                "Некорректная дата"
            )

    # =====================================================
    # FIELD LIMITS
    # =====================================================

    def get_min_date(
        self,
        field,
    ):

        if field.min_value:
            return self.to_date(
                field.min_value
            )

        return self.MIN_DATE

    def get_max_date(
        self,
        field,
    ):

        if field.max_value:
            return self.to_date(
                field.max_value
            )

        return self.MAX_DATE

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_date(
        self,
        field,
        value,
    ):

        parsed = self.to_date(value)

        min_date = self.get_min_date(field)
        max_date = self.get_max_date(field)

        if parsed < min_date:
            raise ValidationError(
                "Дата слишком маленькая"
            )

        if parsed > max_date:
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
                self.validate_date(
                    field,
                    v,
                )
                for v in value
            ]

        return self.validate_date(
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
                self.validate_date(
                    field,
                    v,
                )
                for v in value
            ]

        return self.validate_date(
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

        if value is None:
            return None

        if isinstance(value, datetime):
            value = value.date()

        return self.to_date(value).isoformat()

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

        return self.to_date(value)

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
                    self.to_date(value)
            }
        )

    # =====================================================
    # UI
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(field)

        min_date = self.get_min_date(field)
        max_date = self.get_max_date(field)

        schema.update({

            "inputType":
                "date",

            "min":
                min_date.isoformat(),

            "max":
                max_date.isoformat(),

            "builder": {
                "features":
                    self.features,

                "defaultValueWidget":
                    self.default_value_widget,
            },
        })

        return schema