# =========================================================
# backend/dynamic/field_types/relation.py
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.EntityRegistry import (
    entity_registry,
)

from backend.engine.fields.types.base import (
    BaseFieldType,
)

from backend.engine.fields.types.registry import (
    register_field_type,
)


@register_field_type
class RelationFieldType(
    BaseFieldType
):

    code = "relation"

    label = "Relation"

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        super().validate(
            field,
            value,
        )

        if value in (
            None,
            "",
            [],
        ):
            return

        if not field.relation_entity:

            raise ValidationError(
                "Не задан relation_entity"
            )

        entity = entity_registry.get(
            field.relation_entity
        )

        model = entity.model

        values = (
            value
            if field.is_multiple
            else [value]
        )

        existing = set(
            model.objects.filter(
                pk__in=values
            ).values_list(
                "pk",
                flat=True,
            )
        )

        for item in values:

            if item not in existing:

                raise ValidationError(
                    f"Объект "
                    f"{item} "
                    f"не найден"
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
                int(v)
                for v in value
            ]

        return int(value)

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

        if field.is_multiple:
            items = (
                value.all()
                if hasattr(value, "all")
                else value
            )

            return ", ".join(
                str(x)
                for x in items
            )

        return str(value)
    # =====================================================
    # WIDGET
    # =====================================================

    def get_widget(
        self,
        field,
    ):

        return (
            field.widget
            or (
                "multiselect"
                if field.is_multiple
                else "select"
            )
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        schema = super().get_schema(
            field
        )

        schema.update({

            "relation_entity":
                field.relation_entity,

            "multiple":
                field.is_multiple,
        })

        return schema