# =========================================================
# backend/engine/list/Base/fields.py
# =========================================================

def build_fields(ctx):

    runtime_fields = (
        ctx.entity.get_fields(
            request=ctx.request
        )
        or []
    )

    ctx.runtime_fields = (
        runtime_fields
    )

    allowed = set(
        ctx.entity.list_display
        or []
    )

    fields = []

    for field in runtime_fields:

        # =====================================
        # HIDDEN
        # =====================================

        if field.hidden:
            continue

        # =====================================
        # LIST DISPLAY
        # =====================================

        if (
            allowed
            and field.name
            not in allowed
        ):
            continue

        # =====================================
        # SCHEMA
        # =====================================

        schema = field.get_schema()

        # =====================================
        # RESULT
        # =====================================

        fields.append({

            "key":
                field.name,

            "label":
                schema.get(
                    "label",
                    field.name,
                ),

            "sortable":
                not schema.get(
                    "dynamic",
                    False,
                ),

            "dynamic":
                bool(
                    schema.get(
                        "dynamic",
                        False,
                    )
                ),
        })

    ctx.fields = fields

    return ctx