# =========================================================
# backend/engine/list/Base/search.py
# =========================================================

from django.db.models import Q


def apply_search(ctx):

    q = (
        ctx.request.GET.get("search")
        or ctx.request.GET.get("q")
    )

    if not q:
        return

    entity = ctx.entity

    runtime_fields = (
        ctx.runtime_fields
        or []
    )

    searchable = set(
        getattr(
            entity,
            "search_fields",
            [],
        ) or []
    )

    qs = ctx.qs

    # =====================================================
    # APPLY RUNTIME SEARCH
    # =====================================================

    for field in runtime_fields:

        # =============================================
        # NOT SEARCHABLE
        # =============================================

        if field.name not in searchable:
            continue

        # =============================================
        # FIELD SEARCH
        # =============================================

        qs = field.apply_search(
            qs,
            q,
        )

    ctx.qs = qs