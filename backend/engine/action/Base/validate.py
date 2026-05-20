from django.core.exceptions import (
    ValidationError,
)


def validate(ctx):

    # =====================================================
    # CUSTOM ACTION VALIDATION
    # =====================================================

    payload = ctx.action.validate(

        ctx.request,

        ctx.payload,

        ctx.ctx,
    )

    payload = payload or {}

    # =====================================================
    # RUNTIME VALIDATION
    # =====================================================

    clean = {}

    errors = {}

    for field in (
        ctx.runtime_fields
        or []
    ):

        value = payload.get(
            field.name
        )

        try:

            normalized = (
                field.normalize(
                    value
                )
            )

            field.validate(
                normalized
            )

            clean[field.name] = (
                normalized
            )

        except ValidationError as e:

            errors[field.name] = (

                e.messages

                if hasattr(
                    e,
                    "messages",
                )

                else [str(e)]
            )

    # =====================================================
    # ERRORS
    # =====================================================

    if errors:

        raise ValidationError(
            errors
        )

    # =====================================================
    # RESULT
    # =====================================================

    ctx.data = clean

    return ctx