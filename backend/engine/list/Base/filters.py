def apply_filters(ctx):
    entity = ctx.entity
    allowed = set(getattr(entity, "filter_fields", []) or [])

    if not allowed:
        return

    filters = {}

    for key, value in ctx.request.GET.items():
        if key in {"page", "page_size", "sort", "search", "q"}:
            continue

        if key not in allowed:
            continue

        filters[key] = value

    if filters:
        ctx.qs = ctx.qs.filter(**filters)