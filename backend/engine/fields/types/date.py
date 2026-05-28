# =========================================================
# backend/dynamic/field_types/date.py
# =========================================================

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

    sortable = True

    searchable = False

    filterable = True

    # =====================================================
    # LIMITS
    # =====================================================

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

        parsed = self.parse_date(
            value
        )

        # =============================================
        # RANGE
        # =============================================

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
    # PARSE
    # =====================================================

    def parse_date(
        self,
        value,
    ):

        # =============================================
        # DATE
        # =============================================

        if isinstance(
            value,
            date,
        ) and not isinstance(
            value,
            datetime,
        ):

            return value

        # =============================================
        # DATETIME
        # =============================================

        if isinstance(
            value,
            datetime,
        ):

            return value.date()

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
                "Некорректная дата"
            )

        raw = str(value).strip()

        if not raw:

            raise ValidationError(
                "Некорректная дата"
            )

        # =============================================
        # STRICT ISO DATE
        # YYYY-MM-DD
        # =============================================

        try:

            parsed = date.fromisoformat(
                raw
            )

        except Exception:

            raise ValidationError(
                "Некорректная дата"
            )

        return parsed

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

        return self.parse_date(
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
            or "date"
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
                "date",

            "min":
                self.MIN_DATE.isoformat(),

            "max":
                self.MAX_DATE.isoformat(),
        })

        return schema