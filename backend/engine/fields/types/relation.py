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

        # ================================================
        # MULTIPLE
        # ================================================

        if field.is_multiple:

            if not isinstance(
                value,
                list,
            ):

                raise ValidationError(
                    "Expected list"
                )

            return

        # ================================================
        # SINGLE
        # ================================================

        if isinstance(
            value,
            list,
        ):

            raise ValidationError(
                "Expected single value"
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

            return (
                []
                if field.is_multiple
                else None
            )

        # ================================================
        # ENTITY
        # ================================================

        if not field.relation_entity:

            raise ValidationError(
                "Не задан relation_entity"
            )

        entity = entity_registry.get(
            field.relation_entity
        )

        if not entity:

            raise ValidationError(
                f"Entity "
                f"{field.relation_entity} "
                f"не найдена"
            )

        model = entity.model

        # ================================================
        # MANY
        # ================================================

        if field.is_multiple:

            normalized_ids = []

            for item in value:

                # frontend object
                if isinstance(
                    item,
                    dict,
                ):

                    item = (
                        item.get("value")
                        or item.get("id")
                    )

                try:

                    normalized_ids.append(
                        int(item)
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    raise ValidationError(
                        f"Invalid relation id: "
                        f"{item}"
                    )

            queryset = (
                model.objects.filter(
                    pk__in=normalized_ids
                )
            )

            found_ids = set(
                queryset.values_list(
                    "pk",
                    flat=True,
                )
            )

            missing = (
                set(normalized_ids)
                - found_ids
            )

            if missing:

                raise ValidationError(
                    f"Objects not found: "
                    f"{sorted(missing)}"
                )

            return list(queryset)

        # ================================================
        # SINGLE
        # ================================================

        if isinstance(
            value,
            dict,
        ):

            value = (
                value.get("value")
                or value.get("id")
            )

        try:

            value = int(value)

        except (
            TypeError,
            ValueError,
        ):

            raise ValidationError(
                f"Invalid relation id: "
                f"{value}"
            )

        try:

            return model.objects.get(
                pk=value
            )

        except model.DoesNotExist:

            raise ValidationError(
                f"Object "
                f"{value} "
                f"not found"
            )

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
            self,
            field,
            value,
    ):

        # ================================================
        # EMPTY
        # ================================================

        if value is None:
            return (
                []
                if field.is_multiple
                else None
            )

        # ================================================
        # MANY
        # ================================================

        if field.is_multiple:
            items = (
                value.all()
                if hasattr(value, "all")
                else value
            )

            return [

                {
                    "value": item.pk,
                    "label": str(item),
                }

                for item in items
            ]

        # ================================================
        # SINGLE
        # ================================================

        return {
            "value": value.pk,
            "label": str(value),
        }
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

        options = []

        relation_entity = (
            field.relation_entity
        )

        if relation_entity:

            try:

                entity = entity_registry.get(
                    relation_entity
                )

                queryset = (
                    entity.model.objects.all()
                )

                options = [

                    {
                        "value": obj.pk,
                        "label": str(obj),
                    }

                    for obj in queryset
                ]

            except Exception:

                options = []

        schema.update({

            "relation_entity":
                relation_entity,

            "multiple":
                field.is_multiple,

            "options":
                options,
        })

        return schema