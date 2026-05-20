def serialize(ctx):

    if not ctx.instance:

        ctx.data = {}

        return ctx

    data = {
        "id": ctx.instance.pk,
    }

    for field in ctx.runtime_fields:

        value = field.get_value(
            field.accessor,
            ctx.instance,
        )

        data[field.name] = (
            field.serialize(value)
        )

    ctx.data = data

    return ctx