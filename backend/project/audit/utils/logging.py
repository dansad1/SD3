from backend.project.audit.models import EntityJournal
def serialize_instance(instance):

    if not instance:
        return {}

    data = {}
    for field in instance._meta.fields:
        name = field.name

        try:
            value = getattr(
                instance,
                name,
            )

            if hasattr(value, "pk"):
                value = value.pk

            data[name] = value
        except Exception:
            pass

    return data


def calculate_changes(
    before,
    after,
):

    changes = {}
    before = before or {}
    after = after or {}

    keys = (
        set(before.keys())
        | set(after.keys())
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


def log_entity_event(
    *,
    request,
    action,
    entity,
    instance,
    before=None,
    after=None,
    meta=None,
):

    changes = calculate_changes(
        before,
        after,
    )

    EntityJournal.objects.create(
        actor=(
            request.user
            if (
                request
                and request.user.is_authenticated
            )
            else None
        ),
        action=action,
        entity=entity,
        object_id=str(instance.pk),
        object_repr=str(instance),
        changes=changes,
        meta=meta or {},
    )