import re


def validate_regex(ctx):

    field = ctx.field

    pattern = getattr(
        field,
        "regex",
        None,
    )

    if not pattern:
        return

    value = ctx.value

    if value in (None, ""):
        return

    if not re.match(
        pattern,
        str(value),
    ):
        ctx.errors.append(
            "Invalid format"
        )