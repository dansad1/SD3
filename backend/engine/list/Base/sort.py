def apply_sort(ctx):

    raw = ctx.request.GET.get("sort")

    if not raw:
        return

    if raw.startswith("-"):
        key = raw[1:]
        direction = "desc"
    else:
        key = raw
        direction = "asc"

    field = (
        (ctx.field_map or {})
        .get(key)
    )

    if field:

        custom_sort = getattr(
            field.field_type,
            "apply_sort",
            None,
        )

        if callable(custom_sort):

            qs = custom_sort(
                ctx.qs,
                field,
                direction,
            )

            if qs is not None:
                ctx.qs = qs
                return

    order_key = (
        key
        if direction == "asc"
        else f"-{key}"
    )

    ctx.qs = ctx.qs.order_by(
        order_key
    )