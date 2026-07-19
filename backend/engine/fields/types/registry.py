# =========================================================
# backend/engine/fields/types/registry.py
# =========================================================

from collections.abc import Callable
from typing import Any


FIELD_TYPES = {}

DJANGO_FIELD_TYPES = []

DJANGO_FIELD_RESOLVERS = []


DjangoFieldResolver = Callable[
    [Any],
    str | None,
]


# =========================================================
# FIELD TYPE REGISTER
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
# DJANGO FIELD REGISTER
# =========================================================

def register_django_field(
    *field_classes,
    code,
):
    if not field_classes:
        raise RuntimeError(
            "Django field classes are not specified"
        )

    DJANGO_FIELD_TYPES.append(
        (
            field_classes,
            code,
        )
    )


def register_django_resolver(
    resolver,
):
    DJANGO_FIELD_RESOLVERS.append(
        resolver
    )

    return resolver


# =========================================================
# DJANGO FIELD RESOLVE
# =========================================================

def resolve_django_field_type(
    field,
):
    for resolver in DJANGO_FIELD_RESOLVERS:
        code = resolver(
            field
        )

        if code is not None:
            _check_registered_code(
                code
            )

            return code

    for field_classes, code in DJANGO_FIELD_TYPES:
        if isinstance(
            field,
            field_classes,
        ):
            _check_registered_code(
                code
            )

            return code

    return "string"


def _check_registered_code(
    code,
):
    if code not in FIELD_TYPES:
        raise RuntimeError(
            f"Django field mapping refers "
            f"to unknown field type: {code}"
        )


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