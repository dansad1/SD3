from django.db import models
from django.db.models.fields.reverse_related import (
    ForeignObjectRel,
)

from backend.engine.fields.types.registry import (
    register_django_field,
    register_django_resolver,
)


# =========================================================
# SPECIAL FIELDS
# =========================================================

@register_django_resolver
def resolve_special_field(
    field,
):
    field_name = getattr(
        field,
        "name",
        "",
    )

    if (
        field_name == "password"
        and isinstance(
            field,
            models.CharField,
        )
    ):
        return "password"

    return None


# =========================================================
# FILES
# =========================================================

register_django_field(
    models.ImageField,
    models.FileField,
    code="file",
)


# =========================================================
# RELATIONS
# =========================================================

register_django_field(
    models.ForeignKey,
    models.OneToOneField,
    models.ManyToManyField,
    ForeignObjectRel,
    code="relation",
)


# =========================================================
# SPECIAL STRINGS
# =========================================================

register_django_field(
    models.EmailField,
    code="email",
)


# =========================================================
# TEXT
# =========================================================

register_django_field(
    models.TextField,
    code="text",
)

register_django_field(
    models.CharField,
    models.SlugField,
    models.URLField,
    models.UUIDField,
    code="string",
)


# =========================================================
# NUMBERS
# =========================================================

register_django_field(
    models.SmallIntegerField,
    models.IntegerField,
    models.BigIntegerField,
    models.PositiveIntegerField,
    models.PositiveSmallIntegerField,
    models.FloatField,
    models.DecimalField,
    code="number",
)


# =========================================================
# BOOLEAN
# =========================================================

register_django_field(
    models.BooleanField,
    code="boolean",
)


# =========================================================
# DATE
# =========================================================

register_django_field(
    models.DateTimeField,
    code="datetime",
)

register_django_field(
    models.DateField,
    code="date",
)


# =========================================================
# JSON
# =========================================================

register_django_field(
    models.JSONField,
    code="json",
)