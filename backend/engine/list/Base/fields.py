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

    ctx.field_map = {
        field.name: field
        for field in runtime_fields
    }

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
                bool(
                    getattr(
                        field,
                        "sortable",
                        True,
                    )
                ),

            "dynamic":
                bool(
                    schema.get(
                        "dynamic",
                        False,
                    )
                ),

            "type":
                field.type,

            "readonly":
                field.readonly,

            "hidden":
                field.hidden,
        })

    ctx.fields = fields

    return ctx