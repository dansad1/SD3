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

        print("\n" + "=" * 100)
        print("DynamicValueAccessor.get()")
        print("=" * 100)
        print("Object      :", obj)
        print("Object pk   :", obj.pk)
        print("Field       :", field.name)
        print("Source      :", field.source)
        print("Value model :", value_model)

        # =====================================================
        # NEW STORAGE
        # =====================================================

        if value_model:

            owner = self.get_owner_name(
                obj,
            )

            print("Owner field :", owner)

            qs = (
                value_model.objects
                .select_related("field")
                .filter(
                    **{
                        owner: obj,
                        "field": field.source,
                    }
                )
            )

            print("SQL :", qs.query)
            print("COUNT :", qs.count())

            item = qs.first()

            print("ITEM :", item)

            if not item:
                print("NO VALUE FOUND")
                print("=" * 100)
                return None

            print("RAW DB VALUE :", item.value)

            raw = self.decode(
                item.value,
            )

            print("DECODED :", repr(raw))

            value = field.deserialize(
                raw,
            )

            print("RESULT :", repr(value))
            print("=" * 100)

            return value

        print("USING LEGACY STORAGE")

        content_type = ContentType.objects.get_for_model(
            obj,
            for_concrete_model=False,
        )

        qs = DynamicValue.objects.filter(
            content_type=content_type,
            object_id=obj.pk,
            field_name=field.name,
        )

        print("SQL :", qs.query)
        print("COUNT :", qs.count())

        item = qs.first()

        print("ITEM :", item)

        if not item:
            print("NO LEGACY VALUE")
            print("=" * 100)
            return None

        raw = self.decode(
            item.value,
        )

        print("RAW :", item.value)
        print("DECODED :", repr(raw))

        value = field.deserialize(
            raw,
        )

        print("RESULT :", repr(value))
        print("=" * 100)

        return value
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