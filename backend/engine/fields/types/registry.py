# =========================================================
# backend/dynamic/field_types/registry.py
# =========================================================

FIELD_TYPES = {}


# =========================================================
# REGISTER
# =========================================================

def register_field_type(cls):

    instance = cls()

    FIELD_TYPES[
        instance.code
    ] = instance

    return cls


# =========================================================
# GET
# =========================================================

def get_field_type(code):

    if code not in FIELD_TYPES:

        raise RuntimeError(
            f"Unknown field type: {code}"
        )

    return FIELD_TYPES[code]


# =========================================================
# ALL
# =========================================================

def get_all_field_types():

    return FIELD_TYPES


# =========================================================
# DJANGO CHOICES
# =========================================================

def get_field_type_choices():

    return [

        (
            field_type.code,

            field_type.label,
        )

        for field_type
        in FIELD_TYPES.values()
    ]