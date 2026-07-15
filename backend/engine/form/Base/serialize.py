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
            # VALUE
            # =============================================

            try:

                value = field.get_value(
                    ctx.instance,
                )

            except TypeError:

                value = field.get_value(
                    None,
                    ctx.instance,
                )

            # =============================================
            # DEBUG BEFORE SERIALIZE
            # =============================================

            print("=" * 80)
            print(f"FIELD      : {field.name}")
            print(f"TYPE       : {field.type}")
            print(f"RAW VALUE  : {value!r}")

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
            # DEBUG AFTER SERIALIZE
            # =============================================

            print(f"SERIALIZED : {serialized!r}")
            print("=" * 80)

            # =============================================
            # RESULT
            # =============================================

            data[field.name] = serialized

        except Exception as e:

            print(
                f"[SERIALIZE ERROR] "
                f"field={field.name}: {e}",
            )

            data[field.name] = None

    # =====================================================
    # FINAL DEBUG
    # =====================================================

    print("\n" + "#" * 80)
    print("FINAL DATA")
    print("#" * 80)

    for key, value in data.items():
        print(f"{key}: {value!r}")

    print("#" * 80 + "\n")

    # =====================================================
    # RESULT
    # =====================================================

    ctx.data = data

    return ctx