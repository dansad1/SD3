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
    # RUNTIME FIELDS
    # =====================================================

    runtime_fields = {

        field.name: field

        for field in ctx.runtime_fields

    }

    pre_save_items = []

    post_save_items = []

    # =====================================================
    # SPLIT
    # =====================================================

    for name, value in (
        ctx.data or {}
    ).items():

        field = runtime_fields.get(
            name,
        )

        if not field:
            continue

        # ================================================
        # PASSWORD
        # ================================================

        if (
            field.type == "password"
            and value in (
                None,
                "",
                "********",
            )
        ):
            continue

        if not field.should_save(
            value,
        ):
            continue

        item = (
            field,
            value,
        )

        if field.requires_post_save:

            post_save_items.append(
                item,
            )

        else:

            pre_save_items.append(
                item,
            )

    # =====================================================
    # PRE SAVE
    # =====================================================

    for field, value in pre_save_items:

        field.set_value(
            obj,
            value,
        )

    # =====================================================
    # VALIDATE
    # =====================================================

    obj.full_clean()

    # =====================================================
    # SAVE
    # =====================================================

    obj.save()

    # =====================================================
    # POST SAVE
    # =====================================================

    for field, value in post_save_items:

        field.set_value(
            obj,
            value,
        )

    # =====================================================
    # RESULT
    # =====================================================

    ctx.instance = obj

    return ctx