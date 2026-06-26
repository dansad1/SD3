from django.db.models import Q


def apply_search(ctx):

    q = (
        ctx.request.GET.get("search")
        or ctx.request.GET.get("q")
        or ""
    ).strip()

    if not q:
        return

    entity = ctx.entity

    search_fields = set(
        getattr(
            entity,
            "search_fields",
            [],
        ) or []
    )

    if not search_fields:
        return

    model_field_names = {
        field.name
        for field in ctx.qs.model._meta.get_fields()
    }

    cond = Q()

    for field in entity.get_fields(
            ctx.request,
    ):

        if field.name not in search_fields:
            continue

        if field.name in model_field_names:

            cond |= Q(
                **{
                    f"{field.name}__icontains": q,
                }
            )

            continue

        cond |= Q(
            dynamic_values__field=field.source,
            dynamic_values__value__icontains=q,
        )

    if cond:
        ctx.qs = (
            ctx.qs
            .filter(cond)
            .distinct()
        )