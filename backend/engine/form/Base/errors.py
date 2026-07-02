from django.core.exceptions import ValidationError
from django.utils.encoding import force_str

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

    # Преобразуем ленивые строки Django и обычные строки
    if isinstance(value, str) or hasattr(value, "__proxy__"):
        return force_str(value)

    return force_str(value)


def validation_error_to_dict(exc):

    detail = getattr(
        exc,
        "detail",
        None,
    )

    if detail is None:
        return {
            "__all__": [
                force_str(exc),
            ],
        }

    return normalize_error(detail)