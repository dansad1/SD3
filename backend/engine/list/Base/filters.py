# =========================================================
# backend/engine/list/Base/filters.py
# =========================================================

def apply_filters(ctx):

    entity = ctx.entity

    runtime_fields = (
        ctx.runtime_fields
        or []
    )

    field_map = {
        field.name: field
        for field in runtime_fields
    }

    allowed = set(
        getattr(
            entity,
            "filter_fields",
            [],
        ) or []
    )

    if not allowed:
        return

    qs = ctx.qs

    # =====================================================
    # APPLY FILTERS
    # =====================================================

    for key, value in ctx.request.GET.items():

        # =============================================
        # RESERVED
        # =============================================

        if key in {
            "page",
            "page_size",
            "sort",
            "search",
            "q",
        }:
            continue

        # =============================================
        # NOT ALLOWED
        # =============================================

        if key not in allowed:
            continue

        # =============================================
        # FIELD
        # =============================================

        field = field_map.get(key)

        if not field:
            continue

        # =============================================
        # APPLY
        # =============================================

        qs = field.apply_filter(
            qs,
            value,
        )

    ctx.qs = qs