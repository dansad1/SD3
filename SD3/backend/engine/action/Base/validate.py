def validate(ctx):
    ctx.payload = ctx.action.validate(
        ctx.request,
        ctx.payload,
        ctx.ctx
    )