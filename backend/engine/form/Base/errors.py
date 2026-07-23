from collections.abc import Mapping, Sequence

from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.utils.encoding import force_str
from rest_framework.exceptions import ErrorDetail


def normalize_error(value):
    if isinstance(value, ErrorDetail):
        return force_str(value)

    if isinstance(value, Mapping):
        return {
            force_str(key): normalize_error(item)
            for key, item in value.items()
        }

    if (
        isinstance(value, Sequence)
        and not isinstance(value, (str, bytes))
    ):
        return [
            normalize_error(item)
            for item in value
        ]

    return force_str(value)


def validation_error_to_dict(exc):
    detail = getattr(
        exc,
        "detail",
        None,
    )

    if detail is not None:
        normalized = normalize_error(detail)

        if isinstance(normalized, dict):
            return normalized

        if isinstance(normalized, list):
            return {
                "__all__": normalized,
            }

        return {
            "__all__": [
                normalized,
            ],
        }

    if isinstance(exc, DjangoValidationError):
        if hasattr(exc, "message_dict"):
            return normalize_error(
                exc.message_dict
            )

        if hasattr(exc, "messages"):
            return {
                "__all__": normalize_error(
                    exc.messages
                ),
            }

    return {
        "__all__": [
            force_str(exc),
        ],
    }