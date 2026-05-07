from django.db.models import Q

from backend.engine.entity.Base.queryset import (
    get_queryset
)


# =========================
# SEARCH
# =========================

def apply_search(ctx, qs):

    q = ctx.request.GET.get("q")

    if not q:
        return qs

    fields = (
        ctx.entity.search_fields
        or []
    )

    if not fields:
        return qs

    cond = Q()

    for field in fields:
        cond |= Q(
            **{
                f"{field}__icontains": q
            }
        )

    return qs.filter(cond)


# =========================
# LIMIT
# =========================

def apply_limit(ctx, qs):

    limit = (
        ctx.request.GET.get("limit")
        or 100
    )

    try:
        limit = int(limit)
    except Exception:
        limit = 100

    limit = max(
        1,
        min(limit, 500),
    )

    return qs[:limit]


# =========================
# REPRESENT
# =========================

def serialize_option(
    entity,
    obj,
):

    if hasattr(
        entity,
        "represent_option",
    ):
        return entity.represent_option(obj)

    return {
        "value": obj.pk,
        "label": str(obj),
    }


# =========================
# PIPELINE
# =========================

PIPELINE = [
    apply_search,
    apply_limit,
]


# =========================
# MAIN
# =========================

def get_options(ctx):

    qs = get_queryset(ctx)

    for step in PIPELINE:
        qs = step(ctx, qs)

    return [
        serialize_option(
            ctx.entity,
            obj,
        )
        for obj in qs
    ]