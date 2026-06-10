from .Change import Change
from .ChangeSet import ChangeSet


class ChangeDetector:

    # =====================================================
    # PAYLOAD BASED
    # =====================================================

    def detect(
        self,
        entity,
        request,
        instance,
        payload,
    ):
        changes = ChangeSet()

        fields = entity.get_fields(
            request,
            obj=instance,
        )

        for field in fields:

            name = field.name

            old_value = None

            if instance:

                old_value = (
                    field.get_value(
                        instance
                    )
                )

            if name not in payload:
                continue

            new_value = payload.get(
                name
            )

            if (
                old_value
                ==
                new_value
            ):
                continue

            changes.append(
                Change(
                    field=name,
                    old_value=old_value,
                    new_value=new_value,
                    field_type=field.type,
                    label=field.label,
                )
            )

        return changes

    # =====================================================
    # STATE BASED
    # =====================================================

    def detect_from_state(
        self,
        entity,
        before,
        after,
    ):
        changes = ChangeSet()

        before = before or {}
        after = after or {}

        field_map = {}

        try:

            fields = (
                entity.get_fields(
                    request=None,
                    obj=None,
                )
                or []
            )

            field_map = {
                field.name: field
                for field in fields
            }

        except Exception:

            # аудит не должен ломать сохранение
            field_map = {}

        keys = (
            set(before.keys())
            |
            set(after.keys())
        )

        for key in keys:

            old_value = before.get(key)

            new_value = after.get(key)

            if (
                old_value
                ==
                new_value
            ):
                continue

            field = field_map.get(
                key
            )

            changes.append(
                Change(
                    field=key,

                    old_value=old_value,

                    new_value=new_value,

                    field_type=(
                        field.type
                        if field
                        else None
                    ),

                    label=(
                        field.label
                        if field
                        else key
                    ),
                )
            )

        return changes