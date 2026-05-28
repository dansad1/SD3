# =========================================================
# backend/dynamic/field_types/boolean.py
# =========================================================

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
class BooleanFieldType(BaseFieldType):

    code = "boolean"

    label = "Boolean"

    sortable = True

    searchable = False

    filterable = True

    # =====================================================
    # VALUES
    # =====================================================

    TRUE_VALUES = {

        True,

        1,

        "1",

        "true",

        "True",

        "TRUE",

        "yes",

        "Yes",

        "YES",

        "on",

        "ON",
    }

    FALSE_VALUES = {

        False,

        0,

        "0",

        "false",

        "False",

        "FALSE",

        "no",

        "No",

        "NO",

        "off",

        "OFF",
    }

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
                    "Ожидался список"
                )

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

        if value in self.TRUE_VALUES:

            return True

        if value in self.FALSE_VALUES:

            return False

        raise ValidationError(
            "Некорректное булево значение"
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
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):

        if value is None:

            return None

        return bool(value)

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        if value is None:

            return None

        return self.validate_single(
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

        normalized = (
            self.validate_single(
                value
            )
        )

        return queryset.filter(**{
            field.name: normalized
        })

    # =====================================================
    # UI
    # =====================================================

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or "checkbox"
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
                "checkbox",
        })

        return schema