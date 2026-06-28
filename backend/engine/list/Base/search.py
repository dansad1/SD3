from django.db.models import Q


def apply_search(ctx):

    value = (
        ctx.request.GET.get("search")
        or ctx.request.GET.get("q")
        or ""
    ).strip()

    if not value:
        return

    search_fields = set(
        ctx.entity.search_fields or []
    )

    qs = ctx.qs

    for field in ctx.runtime_fields or []:

        if field.name not in search_fields:
            continue

        qs = field.apply_search(
            qs,
            value,
        )

    ctx.qs = qs.distinct()