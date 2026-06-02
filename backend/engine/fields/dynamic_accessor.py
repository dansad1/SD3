# =========================================================
# dynamic_accessor.py
# =========================================================

from django.contrib.contenttypes.models import (
    ContentType,
)

from backend.engine.fields.value import (
    BaseValueAccessor,
)

from backend.generic.models.DynamicValue import (
    DynamicValue,
)


class DynamicValueAccessor(
    BaseValueAccessor
):

    def get(
        self,
        obj,
        field,
    ):

        content_type = (
            ContentType.objects
            .get_for_model(
                obj,
                for_concrete_model=False,
            )
        )

        value = (

            DynamicValue.objects

            .filter(
                content_type=content_type,
                object_id=obj.pk,
                field_name=field.name,
            )

            .first()
        )

        if not value:
            return None

        return field.deserialize(
            value.value
        )

    def set(
        self,
        obj,
        field,
        value,
    ):

        content_type = (
            ContentType.objects
            .get_for_model(
                obj,
                for_concrete_model=False,
            )
        )

        DynamicValue.objects.update_or_create(

            content_type=content_type,

            object_id=obj.pk,

            field_name=field.name,

            defaults={
                "value":
                    field.serialize(
                        value
                    )
            }
        )

        return value