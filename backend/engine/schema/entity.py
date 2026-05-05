def step_entity(ctx):
    ctx.schema = ctx.entity.customize_field_schema(
        ctx.request,
        ctx.schema,
        field=ctx.field  # 👈 вот это ключ
    )