from django.db import models

def represent(entity, obj, field):

    method = getattr(entity, f"represent_{field}", None)

    if method:
        value = method(obj)
    else:
        value = getattr(obj, field, None)

    # dict
    if isinstance(value, dict):
        return value.get("label", str(value))

    # list
    if isinstance(value, list):
        return ", ".join(
            str(v.get("label") if isinstance(v, dict) else v)
            for v in value
        )

    # file
    if isinstance(value, models.fields.files.FieldFile):
        return value.url if value else ""

    # FK
    if isinstance(value, models.Model):
        return str(value)

    # M2M
    if hasattr(value, "all"):
        return ", ".join(str(item) for item in value.all())

    # bool
    if isinstance(value, bool):
        return "Да" if value else "Нет"

    return value or ""