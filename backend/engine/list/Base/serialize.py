# =========================================================
# backend/engine/list/Base/serialize.py
# =========================================================

def serialize(ctx):

    rows = []

    runtime_fields = (
        ctx.runtime_fields
        or []
    )

    for obj in ctx.page.object_list:

        row = {
            "id": obj.pk,
        }

        for field in runtime_fields:

            # =====================================
            # HIDDEN
            # =====================================

           

            # =====================================
            # LIST DISPLAY
            # =====================================

            allowed = set(
                ctx.entity.list_display
                or []
            )

            if (
                allowed
                and field.name
                not in allowed
            ):
                continue

            # =====================================
            # VALUE
            # =====================================

            value = field.get_value(
                obj
            )

            # =====================================
            # SERIALIZE
            # =====================================

            value = field.serialize(
                value
            )

            # =====================================
            # RESULT
            # =====================================

            row[field.name] = value

        rows.append(row)

    ctx.rows = rows

    return ctx