from django.core.exceptions import ValidationError


def normalize(ctx):

    data = ctx.data or {}

    normalized = {}

    for field in ctx.runtime_fields or []:

        # ============================================
        # SECURITY
        # ============================================

        if field.readonly:
            continue

        name = field.name

        # поле не прислали
        if name not in data:
            continue

        value = data.get(name)

        try:

            normalized_value = (
                field.normalize(value)
            )

        except ValidationError:
            raise

        except Exception as e:

            raise ValidationError({
                name: [str(e)]
            })

        normalized[name] = (
            normalized_value
        )

    ctx.data = normalized

    return ctx