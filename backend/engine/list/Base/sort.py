from django.core.exceptions import FieldError
from django.db.models import F, OuterRef, Subquery

from backend.generic.models import DynamicField


def get_owner_field_name(qs, field):
    value_model = field.value_model

    for model_field in value_model._meta.fields:
        remote_field = getattr(
            model_field,
            "remote_field",
            None,
        )

        if (
            remote_field
            and remote_field.model is qs.model
        ):
            return model_field.name

    return None


def apply_dynamic_sort(
    qs,
    field,
    direction,
):
    value_model = field.value_model

    if value_model is None:
        return qs

    owner_field = get_owner_field_name(
        qs,
        field,
    )

    if not owner_field:
        return qs

    values = (
        value_model.objects
        .filter(
            **{
                f"{owner_field}_id": OuterRef("pk"),
                "field_id": field.source.pk,
            }
        )
        .order_by("pk")
        .values("value")[:1]
    )

    qs = qs.annotate(
        __sort_value=Subquery(
            values,
        )
    )

    if direction == "desc":
        ordering = F(
            "__sort_value",
        ).desc(
            nulls_last=True,
        )
    else:
        ordering = F(
            "__sort_value",
        ).asc(
            nulls_last=True,
        )

    return qs.order_by(
        ordering,
        "pk",
    )


def apply_sort(ctx):
    raw = ctx.request.GET.get(
        "sort",
    )

    if not raw:
        return

    direction = "asc"
    key = raw

    if raw.startswith("-"):
        key = raw[1:]
        direction = "desc"

    field = (
        ctx.field_map
        or {}
    ).get(
        key,
    )

    if field is None:
        return

    if not field.field_type.sortable:
        return

    if isinstance(
        field,
        DynamicField,
    ):
        ctx.qs = apply_dynamic_sort(
            ctx.qs,
            field,
            direction,
        )
        return

    custom_sort = getattr(
        field.field_type,
        "apply_sort",
        None,
    )

    if callable(custom_sort):
        try:
            qs = custom_sort(
                ctx.qs,
                field,
                direction,
            )
        except FieldError:
            qs = None

        if qs is not None:
            ctx.qs = qs
            return

    order = field.name

    if direction == "desc":
        order = f"-{order}"

    try:
        ctx.qs = ctx.qs.order_by(
            order,
            "pk",
        )
    except FieldError as exc:
        print(
            "[SORT ERROR]",
            field.name,
            str(exc),
        )