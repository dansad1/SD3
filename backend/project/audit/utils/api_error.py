from django.http import JsonResponse

from backend.engine.form.Base.errors import (
    validation_error_to_dict,
)

from backend.project.audit.utils.error_logging import (
    log_error,
)


def api_error(
        *,
        request=None,
        message: str,
        type: str = "error",
        status: int = 400,
        field_errors=None,
        exc=None,
):
    if exc:

        try:

            log_error(

                request=request,

                exc=exc,

            )

        except Exception:

            pass

    payload = {

        "status": "error",

        "type": type,

        "message": message,

    }

    if field_errors:

        payload["field_errors"] = (

            field_errors

        )

    return JsonResponse(

        payload,

        status=status,

    )


def api_validation_error(
        exc,
):

    return api_error(

        type="validation",

        message="Ошибка валидации",

        field_errors=(

            validation_error_to_dict(

                exc

            )

        ),

        status=400,

    )


def api_permission_error():

    return api_error(

        type="permission",

        message=(

            "У вас недостаточно "

            "прав для выполнения "

            "данного действия."

        ),

        status=403,

    )


def api_server_error(
        request,
        exc,

):
    return api_error(
        request=request,
        type="server_error",
        message=str(
            exc
        ),
        status=500,
        exc=exc,
    )