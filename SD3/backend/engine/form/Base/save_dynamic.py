from SD3.backend.engine.form.Base.services import save_dynamic_values


def save_dynamic(ctx):
    if not ctx.dynamic:
        return ctx

    save_dynamic_values(
        entity_code=ctx.entity.entity,
        obj=ctx.instance,
        data=ctx.dynamic,
    )

    return ctx