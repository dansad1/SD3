import sys


def step_json(ctx):
    if ctx.type != "json":
        return

    field = ctx.field
    name = ctx.name
    model = ctx.model

    # 🔥 1. Dynamic поле
    if hasattr(field, "field_type"):

        choices = getattr(field, "choices", None)

        if choices:
            parsed = []

            for x in choices.replace("\r", "").split(","):
                x = x.strip()
                if not x:
                    continue

                if "|" in x:
                    value, label = x.split("|", 1)
                    parsed.append({
                        "value": value.strip(),
                        "label": label.strip(),
                    })
                else:
                    parsed.append({
                        "value": x,
                        "label": x,
                    })

            ctx.schema.update({
                "widget": "Select",
                "multiple": True,
                "choices": parsed,
            })

        return  # ❗ ВАЖНО: не идём дальше

    # -------------------------
    # Django логика (как было)
    # -------------------------

    choices = (
        getattr(model, f"{name.upper()}_CHOICES", None)
        or getattr(model, f"{name}_choices", None)
    )

    if not choices:
        module = sys.modules[model.__module__]
        choices = getattr(module, f"{name.upper()}_CHOICES", None)

    if choices:
        ctx.schema.update({
            "widget": "Select",
            "multiple": True,
            "choices": [
                {"value": v, "label": l}
                for v, l in choices
            ]
        })