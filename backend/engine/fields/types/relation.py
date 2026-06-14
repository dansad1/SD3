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

    widget = "select"

    sortable = False
    searchable = False
    filterable = True

    features = [
        "required",
        "relation_entity",
        "is_multiple",
        "help_text",
    ]

    # =====================================================
    # ENTITY
    # =====================================================

    def get_entity_name(
            self,
            field,
    ):

        entity_name = (
                field.options.get("entity")
                or field.options.get(
            "relation_entity"
        )
                or field.options.get(
            "model"
        )
        )

        if entity_name:
            return entity_name

        source = getattr(
            field,
            "source",
            None,
        )

        remote_field = getattr(
            source,
            "remote_field",
            None,
        )

        if not remote_field:
            return None

        related_model = (
            remote_field.model
        )

        related_entity = (
            entity_registry.for_model(
                related_model
            )
        )

        if not related_entity:
            return None

        return related_entity.entity

    def get_entity(
            self,
            field,
    ):

        entity_name = (
            self.get_entity_name(
                field
            )
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

            unique_ids = list(
                dict.fromkeys(ids)
            )

            queryset = (
                model.objects.filter(
                    pk__in=unique_ids
                )
            )

            objects = {
                obj.pk: obj
                for obj in queryset
            }

            missing = (
                    set(unique_ids)
                    - set(
                objects.keys()
            )
            )

            if missing:
                raise ValidationError(
                    f"Objects not found: {sorted(missing)}"
                )

            return [
                objects[obj_id]
                for obj_id in ids
            ]

        object_id = (
            self.extract_id(
                value
            )
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

        object_id = (
            self.extract_id(
                value
            )
        )

        return queryset.filter(
            **{
                field.name:
                    object_id
            }
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
            self,
            field,
            request=None,
            instance=None,
    ):

        schema = super().get_schema(
            field,
            request=request,
            instance=instance,
        )

        schema.update({

            "entity":
                self.get_entity_name(
                    field
                ),

            "lookup":
                True,

        })

        return schema