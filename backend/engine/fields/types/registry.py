# =========================================================
# backend/dynamic/field_types/registry.py
# =========================================================

FIELD_TYPES = {}


def register_field_type(cls):

    FIELD_TYPES[cls.code] = cls()

    return cls


def get_field_type(code):

    if code not in FIELD_TYPES:

        raise RuntimeError(
            f"Unknown field type: {code}"
        )

    return FIELD_TYPES[code]


def get_all_field_types():

    return FIELD_TYPES