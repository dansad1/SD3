from django.db import models
from ckeditor.fields import RichTextField


def step_detect_type(ctx):
    f = ctx.field

    # 🔥 1. Dynamic fields (САМЫЙ ВАЖНЫЙ БЛОК)
    if hasattr(f, "field_type"):
        mapping = {
            "char": "string",
            "string": "string",
            "text": "text",
            "richtext": "richtext",
            "int": "number",
            "integer": "number",
            "bool": "boolean",
            "boolean": "boolean",
            "date": "date",
            "datetime": "datetime",
            "json": "json",
            "choice": "string",          # дальше step_choices решит
            "select": "string",
            "multiselect": "json",       # чаще всего массив
        }

        ctx.type = mapping.get(f.field_type, "string")
        return  # ❗ КРИТИЧНО

    # -------------------------
    # Django fields (как было)
    # -------------------------

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