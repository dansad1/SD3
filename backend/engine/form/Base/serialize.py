# =========================================================
# backend/engine/form/Base/serialize.py
# =========================================================

def serialize(ctx):

    # =====================================================
    # EMPTY
    # =====================================================

    if not ctx.instance:

        ctx.data = {}

        return ctx

    # =====================================================
    # BASE
    # =====================================================

    data = {
        "id": ctx.instance.pk,
    }

    # =====================================================
    # FIELDS
    # =====================================================

    for field in ctx.runtime_fields:

        try:

            # =============================================
            # COMPATIBILITY
            # =============================================

            try:

                value = field.get_value(
                    ctx.instance
                )

            except TypeError:

                value = field.get_value(
                    None,
                    ctx.instance,
                )

            # =============================================
            # SERIALIZE
            # =============================================

            try:

                serialized = field.serialize(
                    value,
                    ctx,
                )

            except TypeError:

                serialized = field.serialize(
                    value,
                )

            # =============================================
            # RESULT
            # =============================================

            data[field.name] = serialized

        except Exception as e:

            print(
                f"[SERIALIZE ERROR] "
                f"field={field.name}:",
                e,
            )

            data[field.name] = None

    # =====================================================
    # RESULT
    # =====================================================

    ctx.data = data

    return ctx