from backend.generic.models import DynamicValue, DynamicField
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery

def apply_dynamic_sort(
        qs,
        field,
        direction,
):

    ct = ContentType.objects.get_for_model(
        qs.model
    )

    values = DynamicValue.objects.filter(

        content_type=ct,

        object_id=OuterRef("pk"),

        field_name=field.name,

    )

    qs = qs.annotate(

        __sort=Subquery(
            values.values(
                "value"
            )[:1]
        )

    )

    order = "__sort"

    if direction == "desc":
        order = "-__sort"

    return qs.order_by(order)

def apply_sort(ctx):

    raw = ctx.request.GET.get("sort")

    if not raw:
        return

    direction = "asc"

    key = raw

    if raw.startswith("-"):
        key = raw[1:]
        direction = "desc"

    field = (
        ctx.field_map or {}
    ).get(key)

    if not field:
        return


    custom = getattr(
        field.field_type,
        "apply_sort",
        None,
    )

    if callable(custom):

        qs = custom(
            ctx.qs,
            field,
            direction,
        )

        if qs is not None:
            ctx.qs = qs
            return


    if isinstance(field, DynamicField):

        ctx.qs = apply_dynamic_sort(

            ctx.qs,

            field,

            direction,

        )

        return


    order = key

    if direction == "desc":
        order = f"-{key}"

    ctx.qs = ctx.qs.order_by(order)