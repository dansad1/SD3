# core/api/generics/ListApi.py

import json
import traceback

from django.http import JsonResponse
from django.views.decorators.http import (
    require_GET,
    require_POST,
)

from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from backend.engine.entity.EntityRegistry import (
    entity_registry,
)

from backend.engine.list.ListRegistry import (
    list_registry,
)

from backend.engine.form.Base.errors import (
    validation_error_to_dict,
)

from backend.project.users.models.UserListSettings import (
    UserListSettings,
)

from backend.project.audit.utils.error_logging import (
    log_error,
)


# =========================================================
# DEBUG
# =========================================================

def print_exception(exc):

    print()
    print("#" * 100)
    print("EXCEPTION")
    print("#" * 100)

    traceback.print_exc()

    print()
    print("TYPE:")
    print(type(exc))

    print()
    print("MESSAGE:")
    print(exc)

    print("#" * 100)
    print()


# =========================================================
# HELPERS
# =========================================================

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

        print_exception(exc)

        try:

            log_error(
                request=request,
                exc=exc,
            )

        except Exception:

            traceback.print_exc()

    payload = {

        "status": "error",

        "type": type,

        "message": message,

    }

    if field_errors:

        payload["field_errors"] = field_errors

    return JsonResponse(
        payload,
        status=status,
    )


# =========================================================
# LIST DATA
# =========================================================

@require_GET
def entity_list_api(
    request,
    entity,
):

    try:

        list_obj = list_registry.get(
            f"{entity}.list",
        )

        result = list_obj.build(
            request,
        )

        return JsonResponse(
            result,
        )

    except ValidationError as e:

        return api_error(
            request=request,
            type="validation",
            message="Ошибка валидации",
            field_errors=validation_error_to_dict(
                e,
            ),
            status=400,
            exc=e,
        )

    except PermissionDenied:

        return api_error(
            request=request,
            type="permission",
            message=(
                "У вас недостаточно прав."
            ),
            status=403,
        )

    except Exception as e:

        return api_error(
            request=request,
            type="server_error",
            message=str(e),
            status=500,
            exc=e,
        )


# =========================================================
# LIST META
# =========================================================

@require_GET
def entity_list_meta_api(
    request,
    entity,
):

    try:

        list_obj = list_registry.get(
            f"{entity}.list",
        )

        fields = list_obj.get_fields(
            request,
        )

        try:

            entity_obj = entity_registry.get(
                entity,
            )

            entity_obj.check_permission(
                request,
                "list",
            )

            default_visible = (
                list_obj.get_default_visible_fields(
                    request,
                )
                or [
                    f["key"]
                    for f in fields
                ]
            )

            settings = (
                UserListSettings.objects
                .filter(
                    user=request.user,
                    entity=entity,
                )
                .first()
            )

            if (
                settings
                and settings.visible_fields
            ):

                visible = (
                    settings.visible_fields
                )

            else:

                visible = default_visible

            capabilities = (
                entity_obj.get_capabilities_for_user(
                    request,
                )
            )

        except KeyError:

            list_obj.check_permission(
                request,
            )

            visible = [
                f["key"]
                for f in fields
            ]

            capabilities = {
                "list": True,
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
            }

        return JsonResponse({

            "entity": entity,

            "fields": fields,

            "visible_fields": visible,

            "capabilities": capabilities,

        })

    except PermissionDenied:

        return api_error(
            request=request,
            type="permission",
            message="У вас недостаточно прав.",
            status=403,
        )

    except Exception as e:

        return api_error(
            request=request,
            type="server_error",
            message=str(e),
            status=500,
            exc=e,
        )


# =========================================================
# LIST SETTINGS
# =========================================================

@require_POST
def entity_list_settings_api(
    request,
    entity,
):

    try:

        data = json.loads(
            request.body or "{}",
        )

        visible_fields = data.get(
            "fields",
            [],
        )

        entity_obj = entity_registry.get(
            entity,
        )

        entity_obj.check_permission(
            request,
            "list",
        )

        UserListSettings.objects.update_or_create(

            user=request.user,

            entity=entity,

            defaults={

                "visible_fields": visible_fields,

            },

        )

        return JsonResponse({

            "status": "ok",

        })

    except PermissionDenied:

        return api_error(
            request=request,
            type="permission",
            message="У вас недостаточно прав.",
            status=403,
        )

    except Exception as e:

        return api_error(
            request=request,
            type="server_error",
            message=str(e),
            status=500,
            exc=e,
        )


# =========================================================
# FILTER META
# =========================================================

@require_GET
def entity_filter_meta_api(
    request,
    entity,
):

    try:

        list_obj = list_registry.get(
            f"{entity}.list",
        )

        fields = list_obj.get_filter_fields(
            request,
        )

        return JsonResponse({

            "entity": entity,

            "fields": fields,

            "saved_filters": [],

        })

    except PermissionDenied:

        return api_error(
            request=request,
            type="permission",
            message="У вас недостаточно прав.",
            status=403,
        )

    except Exception as e:

        return api_error(
            request=request,
            type="server_error",
            message=str(e),
            status=500,
            exc=e,
        )