from backend.engine.schema.builder import EntitySchemaBuilder


def build_schema(ctx):
    builder = EntitySchemaBuilder(ctx.entity)
    schema = builder.build(ctx.request, ctx.mode)

    ctx.fields = schema["fields"]
    ctx.capabilities = schema["capabilities"]

    if ctx.mode == "view":
        for f in ctx.fields:
            f["readonly"] = True