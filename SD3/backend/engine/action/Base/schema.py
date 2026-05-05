def build_schema(ctx):
    ctx.fields = ctx.action.get_fields(ctx.request, ctx.ctx)
    ctx.initial = {}