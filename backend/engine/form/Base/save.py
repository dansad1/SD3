from django.core.exceptions import (
    PermissionDenied,
)


def save(ctx):

    model = ctx.model

    # =====================================================
    # INSTANCE
    # =====================================================

    if ctx.mode == "create":

        obj = model()

    elif ctx.mode == "edit":

        obj = ctx.instance

        if not obj:

            raise PermissionDenied

    else:

        raise PermissionDenied

    # =====================================================
    # SAVE FIELDS
    # =====================================================

    runtime_fields = {

        field.name: field

        for field in ctx.runtime_fields
    }

    for name, value in (
        ctx.data or {}
    ).items():

        field = runtime_fields.get(
            name
        )

        if not field:
            continue

        field.set_value(

            field.accessor,

            obj,

            value,
        )

    # =====================================================
    # DJANGO VALIDATION
    # =====================================================

    obj.full_clean()

    # =====================================================
    # SAVE MODEL
    # =====================================================

    obj.save()

    # =====================================================
    # POST SAVE
    # =====================================================

    for name, value in (
        ctx.data or {}
    ).items():

        field = runtime_fields.get(
            name
        )

        if not field:
            continue

        if getattr(
            field,
            "requires_post_save",
            False,
        ):

            field.set_value(

                field.accessor,

                obj,

                value,
            )

    # =====================================================
    # RESULT
    # =====================================================

    ctx.instance = obj

    return ctx