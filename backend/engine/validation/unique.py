from django.core.exceptions import (
    FieldDoesNotExist
)


def validate_unique(ctx):

    field = ctx.field

    if not getattr(
        field,
        "unique",
        False,
    ):
        return

    value = ctx.value

    if value in (None, ""):
        return

    entity = ctx.entity

    # -------------------------
    # STATIC FIELD
    # -------------------------

    try:

        model_field = (
            entity.model._meta.get_field(
                field.name
            )
        )

        qs = entity.model.objects.filter(
            **{
                field.name: value
            }
        )

        if ctx.instance:
            qs = qs.exclude(
                pk=ctx.instance.pk
            )

        if qs.exists():
            ctx.errors.append(
                "Already exists"
            )

        return

    except FieldDoesNotExist:
        pass

    # -------------------------
    # DYNAMIC FIELD
    # -------------------------

    from backend.users.models import (
        UserFieldValue
    )

    qs = UserFieldValue.objects.filter(
        field=field,
        value=str(value),
    )

    if ctx.instance:
        qs = qs.exclude(
            user=ctx.instance
        )

    if qs.exists():
        ctx.errors.append(
            "Already exists"
        )