from rest_framework.exceptions import ValidationError

from backend.engine.validation.choices import validate_choices
from backend.engine.validation.context import ValidationContext
from backend.engine.validation.regex import validate_regex
from backend.engine.validation.required import validate_required
from backend.engine.validation.unique import validate_unique

PIPELINE = [
    validate_required,
    validate_choices,
    validate_regex,
    validate_unique,
]


def validate_field(
    *,
    field,
    value,
    payload=None,
    request=None,
    entity=None,
    instance=None,
):

    ctx = ValidationContext(
        field=field,
        value=value,
        payload=payload,
        request=request,
        entity=entity,
        instance=instance,
    )

    for step in PIPELINE:
        step(ctx)

    if ctx.errors:
        raise ValidationError(
            ctx.errors
        )

    return value