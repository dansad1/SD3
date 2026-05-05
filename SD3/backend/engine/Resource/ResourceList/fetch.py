def fetch(ctx):
    ctx.result = ctx.resource.get(
        ctx.request,
        **ctx.params
    )