def step_base(ctx):
    field = ctx.field

    label = getattr(
        field,
        "verbose_name",
        getattr(field, "label", ctx.name)
    )

    if hasattr(field, "blank"):
        required = not field.blank
    else:
        required = bool(getattr(field, "required", False))

    ctx.schema = {
        "name": ctx.name,
        "label": str(label),
        "required": required,
        "readonly": False,
    }