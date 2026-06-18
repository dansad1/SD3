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
        "required",
        "placeholder",
        "help_text",
    ]

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

                try:

                    dt = datetime.strptime(
                        raw,
                        "%Y-%m-%d %H:%M:%S",
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
    # VALIDATION
    # =====================================================

    def validate_datetime(
        self,
        value,
    ):
        return self.to_datetime(
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
                self.validate_datetime(v)
                for v in value
            ]

        return self.validate_datetime(
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
                self.validate_datetime(v)
                for v in value
            ]

        return self.validate_datetime(
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

        if dj_timezone.is_naive(
            value
        ):
            value = dj_timezone.make_aware(
                value,
                timezone.utc,
            )

        value = (
            value
            .astimezone(
                timezone.utc
            )
            .replace(
                microsecond=0,
            )
        )

        return value.strftime(
            "%Y-%m-%d %H:%M:%S"
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

        schema["timezone"] = "UTC"

        return schema