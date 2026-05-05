from SD3.backend.engine.form.Base.services import load_dynamic_values


def serialize(ctx):
    rows = []

    for obj in ctx.page.object_list:
        dynamic_values = load_dynamic_values(
            entity_code=ctx.entity.entity,
            obj=obj,
        )

        row = {"id": obj.pk}

        for f in ctx.fields:
            key = f["key"]

            if f.get("dynamic"):
                row[key] = dynamic_values.get(key, "")
            else:
                row[key] = ctx.entity.represent(obj, key)

        rows.append(row)

    ctx.rows = rows