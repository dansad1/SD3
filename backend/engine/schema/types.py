from django.db import models
from ckeditor.fields import RichTextField


def step_detect_type(ctx):

    f = ctx.field

    # =====================================
    # DICT SUPPORT
    # =====================================

    if isinstance(f, dict):

        field_type = (
            f.get("field_type")
            or f.get("type")
            or "string"
        )

        mapping = {
            "char": "string",
            "string": "string",

            # 🔥 NEW
            "password": "password",

            "text": "text",
            "richtext": "richtext",

            "int": "number",
            "integer": "number",

            "bool": "boolean",
            "boolean": "boolean",

            "date": "date",
            "datetime": "datetime",

            "json": "json",

            "choice": "string",
            "select": "string",

            "multiselect": "json",
        }

        ctx.type = mapping.get(
            field_type,
            "string"
        )

        # 🔥 canonical schema
        ctx.schema["type"] = ctx.type

        return

    # =====================================
    # DYNAMIC FIELDS
    # =====================================

    if hasattr(f, "field_type"):

        mapping = {
            "char": "string",
            "string": "string",

            # 🔥 NEW
            "password": "password",

            "text": "text",
            "richtext": "richtext",

            "int": "number",
            "integer": "number",

            "bool": "boolean",
            "boolean": "boolean",

            "date": "date",
            "datetime": "datetime",

            "json": "json",

            "choice": "string",
            "select": "string",

            "multiselect": "json",
        }

        ctx.type = mapping.get(
            f.field_type,
            "string"
        )

        # 🔥 canonical schema
        ctx.schema["type"] = ctx.type

        return

    # =====================================
    # DJANGO FIELDS
    # =====================================

    if isinstance(f, RichTextField):
        ctx.type = "richtext"

    elif isinstance(f, models.ForeignKey):
        ctx.type = "foreignKey"

    elif isinstance(f, models.ManyToManyField):
        ctx.type = "manyToMany"

    elif isinstance(f, models.JSONField):
        ctx.type = "json"

    elif isinstance(f, models.BooleanField):
        ctx.type = "boolean"

    elif isinstance(f, models.DateTimeField):
        ctx.type = "datetime"

    elif isinstance(f, models.DateField):
        ctx.type = "date"

    elif isinstance(f, models.TextField):
        ctx.type = "text"

    else:
        ctx.type = "string"

    # 🔥 canonical schema
    ctx.schema["type"] = ctx.type