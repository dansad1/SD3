def apply_query_initial(ctx):
    request = ctx.request

    query = getattr(request, "query_params", None) or request.GET

    if ctx.mode != "create":
        return

    if ctx.data is None:
        ctx.data = {}

    field_names = {f["name"] for f in (ctx.fields or [])}

    result = {}

    for key, value in query.items():
        if key not in field_names:
            continue

        if value in (None, ""):
            continue

        # каст типов
        if isinstance(value, str) and value.isdigit():
            value = int(value)

        result[key] = value

    # ✅ query = fallback, НЕ override
    ctx.data = {
        **result,
        **(ctx.data or {}),
    }

    print("🔥 APPLY QUERY INITIAL:", result)
    print("🔥 FINAL ctx.data:", ctx.data)