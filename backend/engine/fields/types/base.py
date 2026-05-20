# backend/engine/fields/types/base.py

from django.core.exceptions import ValidationError


class BaseFieldType:

    code = "base"

    label = "Base"

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        if (
            field.required
            and value in (
                None,
                "",
                [],
            )
        ):

            raise ValidationError(
                "Обязательное поле"
            )

        if (
            field.is_multiple
            and not isinstance(
                value,
                list,
            )
        ):

            raise ValidationError(
                "Ожидался список"
            )

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):

        return value

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
            self,
            field,
            value,
    ):
        return value

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        return value

    # =====================================================
    # WIDGET
    # =====================================================

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or self.code
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        return {
            "type": self.code,
            "widget": self.get_widget(
                field
            ),
        }

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        return queryset

    # =====================================================
    # SEARCH
    # =====================================================

    def apply_search(
        self,
        queryset,
        field,
        value,
    ):

        return queryset