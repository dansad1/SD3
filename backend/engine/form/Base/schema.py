from backend.engine.schema.builder import EntitySchemaBuilder


def build_schema(
    ctx,
):
    builder = EntitySchemaBuilder(
        ctx.entity,
    )

    schema = builder.build(
        request=ctx.request,
        fields=ctx.runtime_fields,
        action=ctx.mode,
        obj=ctx.instance,
    )

    ctx.fields = schema["fields"]
    ctx.capabilities = schema["capabilities"]

    if ctx.mode == "view":
        for field in ctx.fields:
            field["readonly"] = True

    return ctx