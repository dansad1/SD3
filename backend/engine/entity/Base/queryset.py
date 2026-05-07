from django.db.models import QuerySet


# =========================
# BASE QUERYSET
# =========================

def build_base_queryset(ctx) -> QuerySet:

    return ctx.entity.model.objects.all()


# =========================
# SOFT DELETE
# =========================

def apply_soft_delete(ctx, qs):

    model = ctx.entity.model

    if (
        ctx.entity.soft_delete
        and hasattr(model, "deleted_at")
    ):
        qs = qs.filter(
            deleted_at__isnull=True
        )

    return qs


# =========================
# SELECT RELATED
# =========================

def apply_select_related(ctx, qs):

    fields = (
        ctx.entity.get_select_related()
        or []
    )

    if fields:
        qs = qs.select_related(*fields)

    return qs


# =========================
# PREFETCH
# =========================

def apply_prefetch_related(ctx, qs):

    fields = (
        ctx.entity.get_prefetch_related()
        or []
    )

    if fields:
        qs = qs.prefetch_related(*fields)

    return qs


# =========================
# USER SCOPE
# =========================

def apply_user_scope(ctx, qs):

    return ctx.entity.apply_user_scope(
        ctx.request,
        qs,
    )


# =========================
# PIPELINE
# =========================

PIPELINE = [
    apply_soft_delete,
    apply_select_related,
    apply_prefetch_related,
    apply_user_scope,
]


# =========================
# MAIN
# =========================

def get_queryset(ctx):

    qs = build_base_queryset(ctx)

    for step in PIPELINE:
        qs = step(ctx, qs)

    return qs