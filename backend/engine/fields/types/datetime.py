# =========================================================
# backend/dynamic/field_types/datetime.py
# =========================================================

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

    sortable = True

    searchable = False

    filterable = True

    # =====================================================
    # LIMITS
    # =====================================================

    MIN_YEAR = 1900

    MAX_YEAR = 2100

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

        if field.is_multiple:

            if not isinstance(
                value,
                list,
            ):

                raise ValidationError(
                    "Ожидался список дат"
                )

            return [
                self.validate_single(v)
                for v in value
            ]

        # =============================================
        # SINGLE
        # =============================================

        return self.validate_single(
            value
        )

    # =====================================================
    # VALIDATE SINGLE
    # =====================================================

    def validate_single(
        self,
        value,
    ):

        dt = self.parse_datetime(
            value
        )

        # =============================================
        # RANGE
        # =============================================

        if dt.year < self.MIN_YEAR:

            raise ValidationError(
                "Дата слишком маленькая"
            )

        if dt.year > self.MAX_YEAR:

            raise ValidationError(
                "Дата слишком большая"
            )

        return dt

    # =====================================================
    # PARSE
    # =====================================================

    def parse_datetime(
        self,
        value,
    ):

        # =============================================
        # DATETIME
        # =============================================

        if isinstance(
            value,
            datetime,
        ):

            dt = value

        else:

            # =========================================
            # TYPE
            # =========================================

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

            # =========================================
            # ISO PARSE
            # =========================================

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

        # =============================================
        # TZ NORMALIZATION
        # =============================================

        if dj_timezone.is_naive(dt):

            dt = dj_timezone.make_aware(
                dt,
                timezone.utc,
            )

        # =============================================
        # UTC
        # =============================================

        dt = dt.astimezone(
            timezone.utc
        )

        return dt

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
                self.validate_single(v)
                for v in value
            ]

        return self.validate_single(
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

        return self.parse_datetime(
            value
        )

    # =====================================================
    # UI
    # =====================================================

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "datetime"
        )

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "inputType":
                "datetime-local",

            "timezone":
                "UTC",
        })

        return schema