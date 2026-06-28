# =========================================================
# backend/engine/list/Base/fields.py
# =========================================================

def build_fields(ctx):

    runtime_fields = (
        ctx.runtime_fields
        or []
    )

    allowed = set(
        ctx.entity.list_display
        or []
    )

    fields = []

    for field in runtime_fields:

        # =====================================
        # LIST DISPLAY
        # =====================================

        if (
            allowed
            and field.name not in allowed
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
                    field.label,
                ),

            "sortable":
                schema.get(
                    "sortable",
                    True,
                ),

            "searchable":
                schema.get(
                    "searchable",
                    False,
                ),

            "filterable":
                schema.get(
                    "filterable",
                    False,
                ),

            "dynamic":
                schema.get(
                    "dynamic",
                    False,
                ),

            "type":
                field.type,

        })

    ctx.fields = fields

    return ctx