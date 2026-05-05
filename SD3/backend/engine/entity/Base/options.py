from django.db.models import Q

from SD3.backend.engine.entity.Base.queryset import get_queryset


def get_options(ctx):
    entity = ctx.entity
    qs = get_queryset(ctx)

    q = ctx.request.GET.get("q")

    if q and entity.search_fields:
        cond = Q()
        for field in entity.search_fields:
            cond |= Q(**{f"{field}__icontains": q})
        qs = qs.filter(cond)

    qs = qs[:100]

    return [
        {"value": obj.pk, "label": str(obj)}
        for obj in qs
    ]