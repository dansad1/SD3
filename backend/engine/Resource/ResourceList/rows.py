def extract_rows(ctx):
    r = ctx.result

    if hasattr(ctx.resource, "get_list_rows"):
        ctx.rows = ctx.resource.get_list_rows(ctx.request, r)
        return

    if isinstance(r, list):
        ctx.rows = r
        return

    if isinstance(r, dict):
        ctx.rows = r.get("rows") or r.get("items") or []
        return

    ctx.rows = []