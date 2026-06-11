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
class RelationFieldType(BaseFieldType):

    code = "relation"

    label = "Relation"

    widget = "select"

    sortable = False

    searchable = False

    filterable = True

    MAX_OPTIONS = 100

    # =====================================================
    # ENTITY
    # =====================================================

    def get_entity_name(
        self,
        field,
    ):

        return (
            field.options.get(
                "entity"
            )
            or field.options.get(
                "relation_entity"
            )
        )

    def get_entity(
        self,
        field,
    ):

        entity_name = self.get_entity_name(
            field
        )

        if not entity_name:

            raise ValidationError(
                "Не задана связанная сущность"
            )

        entity = entity_registry.get(
            entity_name
        )

        if not entity:

            raise ValidationError(
                f"Entity {entity_name} не найдена"
            )

        return entity

    # =====================================================
    # VALUE
    # =====================================================

    def extract_id(
        self,
        value,
    ):

        if isinstance(
            value,
            dict,
        ):

            value = (
                value.get("value")
                or value.get("id")
            )

        try:

            return int(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            raise ValidationError(
                f"Invalid relation id: {value}"
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
            [],
        ):

            return value

        if field.is_multiple:

            if not isinstance(
                value,
                list,
            ):

                raise ValidationError(
                    "Ожидался список"
                )

            return value

        if isinstance(
            value,
            list,
        ):

            raise ValidationError(
                "Ожидалось одно значение"
            )

        return value

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

            return (
                []
                if field.is_multiple
                else None
            )

        entity = self.get_entity(
            field
        )

        model = entity.model

        if field.is_multiple:

            ids = [
                self.extract_id(
                    item
                )
                for item in value
            ]

            queryset = model.objects.filter(
                pk__in=ids
            )

            found_ids = set(
                queryset.values_list(
                    "pk",
                    flat=True,
                )
            )

            missing = (
                set(ids)
                - found_ids
            )

            if missing:

                raise ValidationError(
                    f"Objects not found: {sorted(missing)}"
                )

            return list(
                queryset
            )

        object_id = self.extract_id(
            value
        )

        try:

            return model.objects.get(
                pk=object_id
            )

        except model.DoesNotExist:

            raise ValidationError(
                f"Object {object_id} not found"
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

            return (
                []
                if field.is_multiple
                else None
            )

        if field.is_multiple:

            items = (
                value.all()
                if hasattr(
                    value,
                    "all",
                )
                else value
            )

            return [
                {
                    "value": item.pk,
                    "label": str(item),
                }
                for item in items
            ]

        return {
            "value": value.pk,
            "label": str(value),
        }

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):

        return self.normalize(
            field,
            value,
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
    ):

        entity_name = self.get_entity_name(
            field
        )

        if not entity_name:

            return []

        try:

            entity = entity_registry.get(
                entity_name
            )

        except Exception:

            return []

        if not entity:

            return []

        queryset = (
            entity.model.objects
            .all()
            .order_by("pk")[:self.MAX_OPTIONS]
        )

        return [
            {
                "value": obj.pk,
                "label": str(obj),
            }
            for obj in queryset
        ]

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

        entity_name = self.get_entity_name(
            field
        )

        schema.update({

            "entity":
                entity_name,

            "relation_entity":
                entity_name,

            "multiple":
                field.is_multiple,

            "options":
                self.get_options(
                    field
                ),
        })

        return schema