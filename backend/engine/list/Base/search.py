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

    searchable = set(
        getattr(entity, "search_fields", []) or []
    )

    if not searchable:
        return

    cond = Q()

    for field in searchable:
        cond |= Q(
            **{
                f"{field}__icontains": q
            }
        )

    ctx.qs = ctx.qs.filter(cond)