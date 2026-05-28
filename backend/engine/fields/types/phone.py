# =========================================================
# backend/dynamic/field_types/phone.py
# =========================================================

import phonenumbers

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.types.string import (
    StringFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class PhoneFieldType(StringFieldType):

    code = "phone"

    label = "Phone"

    searchable = True

    sortable = False

    filterable = True

    # =====================================================
    # DEFAULT REGION
    # =====================================================

    DEFAULT_REGION = "UA"

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
                self.validate_single(v)
                for v in value
            ]

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

        if not isinstance(
            value,
            (
                str,
                int,
            ),
        ):

            raise ValidationError(
                "Некорректный номер"
            )

        raw = str(value).strip()

        if not raw:

            raise ValidationError(
                "Некорректный номер"
            )

        try:

            parsed = (
                phonenumbers.parse(
                    raw,
                    self.DEFAULT_REGION,
                )
            )

        except Exception:

            raise ValidationError(
                "Некорректный номер"
            )

        # =============================================
        # VALID
        # =============================================

        if not (
            phonenumbers
            .is_possible_number(
                parsed
            )
        ):

            raise ValidationError(
                "Некорректный номер"
            )

        if not (
            phonenumbers
            .is_valid_number(
                parsed
            )
        ):

            raise ValidationError(
                "Некорректный номер"
            )

        # =============================================
        # E164
        # =============================================

        return (
            phonenumbers.format_number(

                parsed,

                phonenumbers
                .PhoneNumberFormat
                .E164,
            )
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
                self.validate_single(v)
                for v in value
            ]

        return self.validate_single(
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
            or "phone"
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
                "tel",

            "autocomplete":
                "tel",

            "placeholder":
                "+780501234567",

            "format":
                "E.164",
        })

        return schema