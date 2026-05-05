def apply_sort(ctx):
    raw = ctx.request.GET.get("sort")

    if not raw or ":" not in raw:
        return

    key, direction = raw.split(":", 1)

    if direction not in {"asc", "desc"}:
        return

    allowed = set(ctx.entity.list_display or [])

    if allowed and key not in allowed:
        return

    model_fields = {
        f.name
        for f in ctx.entity.model._meta.get_fields()
        if hasattr(f, "attname")
    }

    if key not in model_fields:
        return

    ctx.qs = ctx.qs.order_by(
        f"-{key}" if direction == "desc" else key
    )