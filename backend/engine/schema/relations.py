from backend.engine.entity.EntityRegistry import entity_registry


def step_relations(ctx):
    if ctx.type not in ["foreignKey", "manyToMany"]:
        return

    # 🔥 защита от dynamic
    if not hasattr(ctx.field, "remote_field"):
        return

    model = ctx.field.remote_field.model
    entity = entity_registry.for_model(model)

    ctx.schema["entity"] = (
        entity.entity if entity else model.__name__.lower()
    )

    if ctx.type == "foreignKey":
        ctx.schema["multiple"] = False

    if ctx.type == "manyToMany":
        ctx.schema["multiple"] = True
        ctx.schema["columns"] = 2