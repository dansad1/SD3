from django.db import models


# =========================
# DICT
# =========================

def represent_dict(value):

    return value.get(
        "label",
        str(value),
    )


# =========================
# LIST
# =========================

def represent_list(value):

    return ", ".join(
        str(
            v.get("label")
            if isinstance(v, dict)
            else v
        )
        for v in value
    )


# =========================
# FILE
# =========================

def represent_file(value):

    return value.url if value else ""


# =========================
# MODEL
# =========================

def represent_model(value):

    return str(value)


# =========================
# M2M
# =========================

def represent_m2m(value):

    return ", ".join(
        str(item)
        for item in value.all()
    )


# =========================
# BOOL
# =========================

def represent_bool(value):

    return "Да" if value else "Нет"


# =========================
# VALUE
# =========================

def represent_value(value):

    if isinstance(value, dict):
        return represent_dict(value)

    if isinstance(value, list):
        return represent_list(value)

    if isinstance(
        value,
        models.fields.files.FieldFile,
    ):
        return represent_file(value)

    if isinstance(value, models.Model):
        return represent_model(value)

    if hasattr(value, "all"):
        return represent_m2m(value)

    if isinstance(value, bool):
        return represent_bool(value)

    return value or ""


# =========================
# MAIN
# =========================

def represent(
    entity,
    obj,
    field,
    mode="list",
):

    method = getattr(
        entity,
        f"represent_{field}",
        None,
    )

    if method:
        value = method(obj)
    else:
        value = getattr(
            obj,
            field,
            None,
        )

    return represent_value(value)