def build_meta(ctx):
    r = ctx.result

    if isinstance(r, dict):
        meta = r.get("meta") or r.get("page")
        if meta:
            ctx.meta = meta
            return

    ctx.meta = {
        "page": 1,
        "pages": 1,
        "total": len(ctx.rows),
    }