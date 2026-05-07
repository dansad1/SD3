EMPTY_VALUES = (
    None,
    "",
    [],
)


def validate_required(ctx):

    field = ctx.field

    required = getattr(
        field,
        "required",
        False,
    )

    if not required:
        return

    if ctx.value in EMPTY_VALUES:
        ctx.errors.append(
            "Field required"
        )