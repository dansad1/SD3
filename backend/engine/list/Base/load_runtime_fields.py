# =========================================================
# backend/engine/list/Base/runtime_fields.py
# =========================================================

def load_runtime_fields(ctx):

    runtime_fields = (
        ctx.entity.get_fields(
            request=ctx.request,
        )
        or []
    )

    ctx.runtime_fields = runtime_fields

    ctx.field_map = {
        field.name: field
        for field in runtime_fields
    }

    return ctx