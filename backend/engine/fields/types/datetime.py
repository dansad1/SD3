from datetime import (
    datetime,
    timezone,
)

from django.core.exceptions import (
    ValidationError,
)

from django.utils import timezone as dj_timezone

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class DateTimeFieldType(BaseFieldType):

    code = "datetime"

    label = "DateTime"

    widget = "datetime"

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

    default_value_widget = "datetime"

    MIN_YEAR = 1900
    MAX_YEAR = 2100

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_datetime(
        self,
        value,
    ):

        if isinstance(
            value,
            datetime,
        ):
            dt = value

        else:

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

                dt = datetime.fromisoformat(
                    raw.replace(
                        "Z",
                        "+00:00",
                    )
                )

            except Exception:

                raise ValidationError(
                    "Некорректная дата"
                )

        if dj_timezone.is_naive(dt):

            dt = dj_timezone.make_aware(
                dt,
                timezone.utc,
            )

        return dt.astimezone(
            timezone.utc
        )

    # =====================================================
    # LIMITS
    # =====================================================

    def get_min_datetime(
        self,
        field,
    ):

        if field.min_value:
            return self.to_datetime(
                field.min_value
            )

        return datetime(
            self.MIN_YEAR,
            1,
            1,
            tzinfo=timezone.utc,
        )

    def get_max_datetime(
        self,
        field,
    ):

        if field.max_value:
            return self.to_datetime(
                field.max_value
            )

        return datetime(
            self.MAX_YEAR,
            12,
            31,
            23,
            59,
            59,
            tzinfo=timezone.utc,
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate_datetime(
        self,
        field,
        value,
    ):

        dt = self.to_datetime(
            value
        )

        min_dt = self.get_min_datetime(
            field
        )

        max_dt = self.get_max_datetime(
            field
        )

        if dt < min_dt:
            raise ValidationError(
                "Дата слишком маленькая"
            )

        if dt > max_dt:
            raise ValidationError(
                "Дата слишком большая"
            )

        return dt

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
                self.validate_datetime(
                    field,
                    v,
                )
                for v in value
            ]

        return self.validate_datetime(
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
                self.validate_datetime(
                    field,
                    v,
                )
                for v in value
            ]

        return self.validate_datetime(
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

        if dj_timezone.is_naive(
            value
        ):
            value = dj_timezone.make_aware(
                value,
                timezone.utc,
            )

        value = value.astimezone(
            timezone.utc
        )

        return (
            value
            .isoformat()
            .replace(
                "+00:00",
                "Z",
            )
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

        return self.to_datetime(
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
                    self.to_datetime(
                        value
                    )
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

        min_dt = self.get_min_datetime(
            field
        )

        max_dt = self.get_max_datetime(
            field
        )

        schema.update({

            "inputType":
                "datetime",

            "timezone":
                "UTC",

            "min":
                min_dt.isoformat(),

            "max":
                max_dt.isoformat(),

            "builder": {

                "features":
                    self.features,

                "defaultValueWidget":
                    self.default_value_widget,

            }

        })

        return schema