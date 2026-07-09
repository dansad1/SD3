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

            try:

                return field.deserialize(
                    raw,
                )

            except Exception as exc:

                print("\n" + "=" * 100)
                print("DESERIALIZE ERROR (NEW STORAGE)")
                print("=" * 100)
                print("Owner model :", obj.__class__.__name__)
                print("Owner pk    :", obj.pk)
                print("Field       :", field.name)
                print("Value model :", value_model.__name__)
                print("Raw value   :", item.value)
                print("Decoded     :", raw)
                print("Exception   :", repr(exc))
                print("=" * 100 + "\n")

                raise

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

        try:

            return field.deserialize(
                raw,
            )

        except Exception as exc:

            print("\n" + "=" * 100)
            print("DESERIALIZE ERROR (LEGACY STORAGE)")
            print("=" * 100)
            print("Owner model :", obj.__class__.__name__)
            print("Owner pk    :", obj.pk)
            print("Field       :", field.name)
            print("ContentType :", content_type)
            print("DynamicValue:", item.pk)
            print("Raw value   :", item.value)
            print("Decoded     :", raw)
            print("Exception   :", repr(exc))
            print("=" * 100 + "\n")

            raise
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

            if obj.pk is None:
                raise RuntimeError(
                    f"{obj.__class__.__name__} must be saved "
                    f"before saving dynamic values."
                )

            if (
                    getattr(
                        field.source,
                        "pk",
                        None,
                    )
                    is None
            ):
                raise RuntimeError(
                    f"Dynamic field '{field.name}' "
                    f"is not saved."
                )

            lookup = {
                f"{owner}_id": obj.pk,
                "field_id": field.source.pk,
            }

            item, _ = (
                value_model.objects
                .get_or_create(
                    **lookup,
                )
            )

            item.value = encoded

            item.save(
                update_fields=[
                    "value",
                ],
            )

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