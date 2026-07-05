from django.core.exceptions import ValidationError

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

    widget = "checkbox"

    sortable = True
    searchable = False
    filterable = True

    features = [
        "help_text",
        "required",
    ]

    TRUE_VALUES = {
        True,
        1,
        "1",
        "true",
        "yes",
        "on",
        "✓",
    }

    FALSE_VALUES = {
        False,
        0,
        "0",
        "false",
        "no",
        "off",
        "✗",
        "",
        None,
    }

    # =====================================================
    # CONVERSION
    # =====================================================

    def to_bool(
        self,
        value,
    ):

        if isinstance(value, str):
            value = value.strip().lower()

        if value in self.TRUE_VALUES:
            return True

        if value in self.FALSE_VALUES:
            return False

        raise ValidationError(
            f"Некорректное булево значение: {value!r}"
        )

    # =====================================================
    # VALIDATION
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
            return None

        if field.is_multiple:
            return [
                self.to_bool(v)
                for v in value
            ]

        return self.to_bool(value)

    # =====================================================
    # NORMALIZATION
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
                self.to_bool(v)
                for v in value
            ]

        return self.to_bool(value)

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):

        if value is None:
            return None

        if field.is_multiple:
            return [
                self.to_bool(v)
                for v in value
            ]

        return self.to_bool(value)

    # =====================================================
    # DESERIALIZATION
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

        if field.is_multiple:
            return [
                self.to_bool(v)
                for v in value
            ]

        return self.to_bool(value)

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
                field.name: self.to_bool(value),
            }
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field,
        )

        schema["inputType"] = "checkbox"

        return schema