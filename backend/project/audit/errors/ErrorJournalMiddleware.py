from django.core.exceptions import (
    PermissionDenied,
    ValidationError,
)

from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
)

from backend.project.audit.utils.error_logging import (
    log_error,
)


class ErrorJournalMiddleware:
    def __init__(
            self,
            get_response,
    ):
        self.get_response = (
            get_response
        )

    def __call__(
            self,
            request,
    ):

        try:

            return self.get_response(
                request
            )

        except (
            PermissionDenied,
            ValidationError,
            DRFValidationError,

        ):

            raise
        except Exception as exc:
            log_error(
                request=request,
                exc=exc,
            )

            raise