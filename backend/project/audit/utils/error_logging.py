import traceback

from backend.project.audit.models import ErrorJournal


MAX_FRAMES = 30

def get_client_ip(request):
    forwarded = request.META.get(
        "HTTP_X_FORWARDED_FOR"
    )

    if forwarded:
        return (
            forwarded
            .split(",")[0]
            .strip()
        )

    return request.META.get(
        "REMOTE_ADDR"
    )


def format_traceback(exc):
    frames = traceback.extract_tb(
        exc.__traceback__
    )
    frames = frames[-MAX_FRAMES:]
    tb = "".join(
        traceback.format_list(
            frames
        )
    )
    tb += "\n"
    tb += "".join(
        traceback.format_exception_only(
            type(exc),
            exc,
        )
    )
    return tb


def log_error(
        request,
        exc,
):

    ErrorJournal.objects.create(
        user=(
            request.user
            if (
                hasattr(
                    request,
                    "user",
                )
                and request.user.is_authenticated
            )

            else None
        ),
        exception=type(exc).__name__,
        message=str(exc),
        traceback=format_traceback(
            exc
        ),
        path=request.path,
        method=request.method,
        ip=get_client_ip(
            request
        ),
        meta={
            "query": dict(
                request.GET
            ),

        },

    )