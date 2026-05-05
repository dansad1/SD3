def execute(ctx):
    ctx.result = ctx.action.run(
        ctx.request,
        ctx.payload,
        ctx.ctx
    )