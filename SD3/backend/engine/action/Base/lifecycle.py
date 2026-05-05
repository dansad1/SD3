def before(ctx):
    ctx.action.before(ctx.request, ctx.payload, ctx.ctx)

def after(ctx):
    ctx.action.after(ctx.request, ctx.result, ctx.ctx)