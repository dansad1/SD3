from django.core.exceptions import ValidationError
from rest_framework.exceptions import ErrorDetail


def normalize_error(value):

    if isinstance(value, ErrorDetail):
        return str(value)

    if isinstance(value, list):
        return [
            normalize_error(v)
            for v in value
        ]

    if isinstance(value, dict):
        return {
            k: normalize_error(v)
            for k, v in value.items()
        }

    return value


def validation_error_to_dict(exc):

    detail = getattr(
        exc,
        "detail",
        None,
    )

    if detail is None:
        return {
            "__all__": [str(exc)]
        }

    return normalize_error(detail)