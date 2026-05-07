import json


def parse_choices(choices):

    if not choices:
        return []

    if isinstance(
        choices,
        (list, tuple),
    ):
        return [
            x[0]
            if isinstance(x, tuple)
            else x
            for x in choices
        ]

    return [
        x.strip()
        for x in choices
        .replace("\r", "")
        .split(",")
        if x.strip()
    ]


def validate_choices(ctx):

    field = ctx.field

    choices = getattr(
        field,
        "choices",
        None,
    )

    if not choices:
        return

    allowed = parse_choices(
        choices
    )

    value = ctx.value

    multiple = getattr(
        field,
        "is_multiple",
        False,
    )

    if multiple:

        if not isinstance(
            value,
            list,
        ):
            ctx.errors.append(
                "Expected list"
            )
            return

        invalid = [
            x
            for x in value
            if x not in allowed
        ]

        if invalid:
            ctx.errors.append(
                f"Invalid choices: {invalid}"
            )

        return

    if value not in allowed:
        ctx.errors.append(
            "Invalid choice"
        )