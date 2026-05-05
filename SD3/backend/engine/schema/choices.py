def step_choices(ctx):
    field = ctx.field

    choices = getattr(field, "choices", None)

    if not choices:
        return

    # 🔥 1. Dynamic (строка)
    if isinstance(choices, str):
        parsed = [
            x.strip()
            for x in choices.replace("\r", "").split(",")
            if x.strip()
        ]

        ctx.schema["choices"] = [
            {"value": v, "label": v}
            for v in parsed
        ]

    # 🔥 2. Django (tuple list)
    else:
        ctx.schema["choices"] = [
            {"value": v, "label": l}
            for v, l in choices
        ]

    # 🔥 widget логика (оставляем твою)
    if ctx.type == "manyToMany" or ctx.type == "json":
        ctx.schema["widget"] = "MultiSelect"
    else:
        ctx.schema["widget"] = "Select"