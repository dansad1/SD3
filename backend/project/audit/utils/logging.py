from datetime import (
    datetime,
    date,
    time,
)

from decimal import Decimal
from uuid import UUID

from backend.project.audit.models.EntityJournal import (
    EntityJournal,
)


# =========================================================
# JSON SAFE
# =========================================================

def make_json_safe(value):

    if isinstance(value, dict):
        return {
            k: make_json_safe(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [
            make_json_safe(v)
            for v in value
        ]

    if isinstance(value, (datetime, date, time)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return str(value)

    if isinstance(value, UUID):
        return str(value)

    if hasattr(value, "pk"):
        return value.pk

    return value


# =========================================================
# SERIALIZATION
# =========================================================

def serialize_instance(instance):

    if not instance:
        return {}

    data = {}

    for field in instance._meta.fields:

        try:

            value = getattr(
                instance,
                field.name,
            )

            data[field.name] = (
                make_json_safe(value)
            )

        except Exception:
            pass

    return data


# =========================================================
# CHANGES
# =========================================================

def calculate_changes(
    before,
    after,
):

    changes = {}

    before = before or {}
    after = after or {}

    keys = (
        set(before.keys())
        |
        set(after.keys())
    )

    for key in keys:

        old = before.get(key)
        new = after.get(key)

        if old != new:

            changes[key] = {
                "before": old,
                "after": new,
            }

    return changes


# =========================================================
# AUDIT LOG
# =========================================================

def log_entity_event(
    *,
    request,
    action,
    entity,
    instance=None,
    before=None,
    after=None,
    meta=None,
):

    changes = calculate_changes(
        before,
        after,
    )

    changes = make_json_safe(
        changes
    )

    meta = make_json_safe(
        meta or {}
    )

    if (
        action == "update"
        and not changes
        and not meta
    ):
        return None

    object_id = (
        meta.get("object_id")
        or getattr(
            instance,
            "pk",
            None,
        )
    )

    object_repr = (
        meta.get("object_repr")
        or (
            str(instance)
            if instance
            else ""
        )
    )

    return EntityJournal.objects.create(

        actor=(
            request.user
            if (
                request
                and hasattr(
                    request,
                    "user",
                )
                and request.user.is_authenticated
            )
            else None
        ),
        action=action,
        entity=entity,
        object_id=str(
            object_id
        ),
        object_repr=object_repr,
        changes=changes,

        meta=meta,
    )