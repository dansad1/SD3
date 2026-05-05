from django.db.models import Q


def apply_search(ctx):
    q = ctx.request.GET.get("search") or ctx.request.GET.get("q")

    if not q:
        return

    entity = ctx.entity
    model = entity.model

    fields = getattr(entity, "search_fields", None) or []

    model_fields = {
        f.name
        for f in model._meta.get_fields()
        if hasattr(f, "attname")
    }

    cond = Q()

    for field in fields:
        if field not in model_fields:
            continue

        cond |= Q(**{f"{field}__icontains": q})

    if cond.children:
        ctx.qs = ctx.qs.filter(cond)