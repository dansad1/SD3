# =========================================================
# backend/engine/fields/types/registry.py
# =========================================================

FIELD_TYPES = {}


# =========================================================
# REGISTER
# =========================================================

def register_field_type(cls):

    instance = cls()

    code = getattr(
        instance,
        "code",
        None,
    )

    if not code:

        raise RuntimeError(
            f"Field type {cls.__name__} "
            f"does not define code"
        )

    if code in FIELD_TYPES:

        raise RuntimeError(
            f"Field type '{code}' "
            f"already registered"
        )

    FIELD_TYPES[code] = instance

    return cls


# =========================================================
# GET
# =========================================================

def get_field_type(code):

    if hasattr(
        code,
        "code",
    ):
        return code

    if not code:

        raise RuntimeError(
            "Field type is empty"
        )

    try:

        return FIELD_TYPES[
            code
        ]

    except KeyError:

        raise RuntimeError(
            f"Unknown field type: {code}. "
            f"Available: "
            f"{', '.join(sorted(FIELD_TYPES))}"
        )


# =========================================================
# EXISTS
# =========================================================

def has_field_type(code):

    return code in FIELD_TYPES


# =========================================================
# ALL
# =========================================================

def get_all_field_types():

    return dict(
        FIELD_TYPES
    )


# =========================================================
# CODES
# =========================================================

def get_field_type_codes():

    return sorted(
        FIELD_TYPES.keys()
    )


# =========================================================
# DJANGO CHOICES
# =========================================================

def get_field_type_choices():

    return sorted(

        [
            (
                field_type.code,
                field_type.label,
            )

            for field_type
            in FIELD_TYPES.values()
        ],

        key=lambda item: item[1],
    )