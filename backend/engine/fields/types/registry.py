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

    # =============================================
    # ALREADY RESOLVED
    # =============================================

    if hasattr(
        code,
        "code",
    ):
        return code

    # =============================================
    # EMPTY
    # =============================================

    if not code:

        raise RuntimeError(
            "Field type is empty"
        )

    # =============================================
    # LOOKUP
    # =============================================

    field_type = FIELD_TYPES.get(
        code
    )

    if field_type:

        return field_type

    raise RuntimeError(
        f"Unknown field type: {code}. "
        f"Available: "
        f"{', '.join(sorted(FIELD_TYPES.keys()))}"
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

    return FIELD_TYPES


# =========================================================
# CODES
# =========================================================

def get_field_type_codes():

    return list(
        FIELD_TYPES.keys()
    )


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