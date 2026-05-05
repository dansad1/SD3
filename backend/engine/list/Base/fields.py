from SD3.backend.engine.schema.builder import EntitySchemaBuilder


def build_fields(ctx):
    builder = EntitySchemaBuilder(ctx.entity)
    schema = builder.build(ctx.request, action="view")

    allowed = set(ctx.entity.list_display or [])

    fields = []

    for f in schema["fields"]:
        name = f["name"]

        if allowed and name not in allowed:
            continue

        fields.append({
            "key": name,
            "label": f["label"],
            "sortable": not f.get("dynamic", False),
            "dynamic": bool(f.get("dynamic", False)),
        })

    ctx.fields = fields