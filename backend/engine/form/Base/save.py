from django.core.exceptions import (
    PermissionDenied,
)


def save(ctx):

    print("\n" + "=" * 100)
    print("SAVE")
    print("=" * 100)
    print("MODE:", ctx.mode)
    print("CTX.DATA:", repr(ctx.data))
    print("=" * 100)

    model = ctx.model

    if ctx.mode == "create":

        obj = model()

    elif ctx.mode == "edit":

        obj = ctx.instance

        if not obj:
            raise PermissionDenied

    else:

        raise PermissionDenied

    runtime_fields = {
        field.name: field
        for field in ctx.runtime_fields
    }

    print("RUNTIME FIELDS:")
    for field in ctx.runtime_fields:
        print(
            field.name,
            field.type,
            field.requires_post_save,
        )

    pre_save_items = []
    post_save_items = []

    for name, value in (ctx.data or {}).items():

        print(
            "INPUT:",
            name,
            repr(value),
        )

        field = runtime_fields.get(name)

        if not field:
            print("  -> FIELD NOT FOUND")
            continue

        if (
            field.type == "password"
            and value in (
                None,
                "",
                "********",
            )
        ):
            print("  -> PASSWORD SKIP")
            continue

        if not field.should_save(value):
            print("  -> SHOULD_SAVE = FALSE")
            continue

        if field.requires_post_save:

            print("  -> POST SAVE")

            post_save_items.append(
                (field, value),
            )

        else:

            print("  -> PRE SAVE")

            pre_save_items.append(
                (field, value),
            )

    print("\nPRE SAVE ITEMS:")
    for field, value in pre_save_items:
        print(field.name, repr(value))

    print("\nPOST SAVE ITEMS:")
    for field, value in post_save_items:
        print(field.name, repr(value))

    for field, value in pre_save_items:

        print("PRE:", field.name)

        field.set_value(
            obj,
            value,
        )

    obj.full_clean()
    obj.save()

    print("OBJECT PK:", obj.pk)

    for field, value in post_save_items:

        print("POST:", field.name)

        field.set_value(
            obj,
            value,
        )

    print("=" * 100)

    ctx.instance = obj

    return ctx