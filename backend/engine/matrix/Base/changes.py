def extract_changes(ctx):
    payload = ctx.payload
    ctx.changes = payload.get("changes") or payload