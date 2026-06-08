# engine/changes/ChangeDetector.py

from .Change import Change
from .ChangeSet import ChangeSet


class ChangeDetector:

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