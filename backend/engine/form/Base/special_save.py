def save_special_fields(
    ctx,
):
    for field in ctx.runtime_fields or []:
        value = ctx.data.get(
            field.name,
        )

        field_type = field.field_type

        if field_type.should_save(
            field,
            value,
        ):
            continue

        if not value:
            continue

        save_method = getattr(
            field_type,
            "save",
            None,
        )

        if not save_method:
            continue

        save_method(
            instance=ctx.instance,
            field=field,
            value=value,
            request=ctx.request,
        )

    return ctx