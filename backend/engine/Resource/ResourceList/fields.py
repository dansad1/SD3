from SD3.backend.engine.Resource.ResourceList.field_policy import resolve_entity, allow_field


def build_fields(ctx):

    r = ctx.result
    resource = ctx.resource
    entity = resolve_entity(resource)

    fields = None

    # 1. explicit
    if hasattr(resource, "get_list_fields"):
        fields = resource.get_list_fields(ctx.request, r)

    # 2. sample row
    if not fields and ctx.rows and isinstance(ctx.rows[0], dict):
        fields = [
            {
                "key": k,
                "label": k.replace("_", " ").capitalize(),
            }
            for k in ctx.rows[0].keys()
            if not k.endswith("_id")
        ]

    # 3. empty row
    if not fields and hasattr(resource, "get_empty_row"):
        empty = resource.get_empty_row(ctx.request)
        if isinstance(empty, dict):
            fields = [
                {
                    "key": k,
                    "label": k.replace("_", " ").capitalize(),
                }
                for k in empty.keys()
            ]

    if not fields:
        ctx.fields = []
        return

    # 🔥 КЛЮЧ: фильтрация
    ctx.fields = [
        f for f in fields
        if allow_field(resource, entity, f["key"])
    ]