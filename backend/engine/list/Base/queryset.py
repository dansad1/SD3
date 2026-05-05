def load_queryset(ctx):
    ctx.qs = ctx.entity.get_queryset(ctx.request)