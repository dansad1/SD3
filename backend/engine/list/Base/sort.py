# =========================================================
# backend/engine/list/Base/sort.py
# =========================================================

def apply_sort(ctx):

    raw = ctx.request.GET.get(
        "sort"
    )

    if (
        not raw
        or ":" not in raw
    ):
        return

    # =====================================================
    # PARSE
    # =====================================================

    key, direction = raw.split(
        ":",
        1,
    )

    if direction not in {
        "asc",
        "desc",
    }:
        return

    # =====================================================
    # LIST DISPLAY VALIDATION
    # =====================================================

    allowed = set(
        ctx.entity.list_display
        or []
    )

    if (
        allowed
        and key not in allowed
    ):
        return

    # =====================================================
    # FIELD MAP
    # =====================================================

    field_map = (
        ctx.field_map
        or {}
    )

    field = field_map.get(key)

    if not field:
        return

    # =====================================================
    # SORTABLE VALIDATION
    # =====================================================

    if not getattr(
        field,
        "sortable",
        True,
    ):
        return

    # =====================================================
    # APPLY FIELD SORT
    # =====================================================

    qs = field.field_type.apply_sort(
        ctx.qs,
        field,
        direction,
    )

    if qs is not None:
        ctx.qs = qs