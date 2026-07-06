import json

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
    BaseValueAccessor,
):

    # =====================================================
    # HELPERS
    # =====================================================

    def get_value_model(
        self,
        field,
    ):
        return getattr(
            field,
            "value_model",
            None,
        )

    def get_owner_name(
        self,
        obj,
    ):
        return obj._meta.model_name

    # =====================================================
    # STORAGE
    # =====================================================

    def encode(
        self,
        value,
    ):
        if value is None:
            return None

        if isinstance(
            value,
            (dict, list),
        ):
            return json.dumps(
                value,
                ensure_ascii=False,
            )

        return str(value)

    def decode(
        self,
        value,
    ):
        if value in (
            None,
            "",
        ):
            return None

        if not isinstance(
            value,
            str,
        ):
            return value

        try:
            return json.loads(
                value,
            )
        except (
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):
            return value

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        obj,
        field,
    ):
        value_model = self.get_value_model(
            field,
        )

        # ===============================================
        # NEW STORAGE
        # ===============================================

        if value_model:

            owner = self.get_owner_name(
                obj,
            )

            item = (
                value_model.objects
                .select_related(
                    "field",
                )
                .filter(
                    **{
                        owner: obj,
                        "field": field.source,
                    }
                )
                .first()
            )

            if not item:
                return None

            raw = self.decode(
                item.value,
            )

            return field.deserialize(
                raw,
            )

        # ===============================================
        # LEGACY STORAGE
        # ===============================================

        content_type = (
            ContentType.objects.get_for_model(
                obj,
                for_concrete_model=False,
            )
        )

        item = (
            DynamicValue.objects
            .filter(
                content_type=content_type,
                object_id=obj.pk,
                field_name=field.name,
            )
            .first()
        )

        if not item:
            return None

        raw = self.decode(
            item.value,
        )

        return field.deserialize(
            raw,
        )

    # =====================================================
    # SET
    # =====================================================

    def set(
        self,
        obj,
        field,
        value,
    ):
        value_model = self.get_value_model(
            field,
        )

        serialized = field.serialize(
            value,
        )

        encoded = self.encode(
            serialized,
        )

        # ===============================================
        # NEW STORAGE
        # ===============================================

        if value_model:

            owner = self.get_owner_name(
                obj,
            )

            item, _ = (
                value_model.objects
                .get_or_create(
                    **{
                        owner: obj,
                        "field": field.source,
                    }
                )
            )

            item.value = encoded
            item.save()

            return value

        # ===============================================
        # LEGACY STORAGE
        # ===============================================

        content_type = (
            ContentType.objects.get_for_model(
                obj,
                for_concrete_model=False,
            )
        )

        DynamicValue.objects.update_or_create(
            content_type=content_type,
            object_id=obj.pk,
            field_name=field.name,
            defaults={
                "value": encoded,
            },
        )

        return value