# core/api/generics/ListApi.py

import json

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


# =========================================================
# HELPERS
# =========================================================

def api_error(
    *,
    message: str,
    type: str = "error",
    status: int = 400,
    field_errors=None,
):

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


# =========================================================
# LIST DATA
# =========================================================

@require_GET
def entity_list_api(
    request,
    entity: str,
):

    try:

        list_obj = list_registry.get(
            f"{entity}.list"
        )

        result = list_obj.build(
            request
        )

        return JsonResponse(result)

    # =====================================================
    # VALIDATION
    # =====================================================

    except ValidationError as e:

        return api_error(
            type="validation",
            message="Ошибка валидации",
            field_errors=(
                validation_error_to_dict(e)
            ),
            status=400,
        )

    # =====================================================
    # PERMISSION
    # =====================================================

    except PermissionDenied:

        return api_error(
            type="permission",
            message=(
                "У вас недостаточно "
                "прав для выполнения "
                "данного действия."
            ),
            status=403,
        )

    # =====================================================
    # UNKNOWN
    # =====================================================

    except Exception as e:

        return api_error(
            type="server_error",
            message=str(e),
            status=500,
        )


# =========================================================
# SETTINGS
# =========================================================

class UserListSettings:
    pass


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
            f"{entity}.list"
        )

        fields = list_obj.get_fields(
            request
        )

        # =============================================
        # ENTITY LIST
        # =============================================

        try:

            entity_obj = entity_registry.get(
                entity
            )

            entity_obj.check_permission(
                request,
                "list",
            )

            default_visible = (

                list_obj
                .get_default_visible_fields(
                    request
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
                settings and
                settings.visible_fields
            ):

                visible = (
                    settings.visible_fields
                )

            else:

                visible = (
                    default_visible
                )

            capabilities = (
                entity_obj
                .get_capabilities_for_user(
                    request
                )
            )

        except KeyError:

            # =========================================
            # RESOURCE LIST
            # =========================================

            list_obj.check_permission(
                request
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
            type="permission",
            message=(
                "У вас недостаточно "
                "прав для выполнения "
                "данного действия."
            ),
            status=403,
        )

    except Exception as e:

        return api_error(
            type="server_error",
            message=str(e),
            status=500,
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
            request.body or "{}"
        )

        visible_fields = data.get(
            "fields",
            [],
        )

        entity_obj = entity_registry.get(
            entity
        )

        entity_obj.check_permission(
            request,
            "list",
        )

        UserListSettings.objects.update_or_create(
            user=request.user,
            entity=entity,
            defaults={
                "visible_fields":
                    visible_fields
            },
        )

        return JsonResponse({
            "status": "ok"
        })

    except PermissionDenied:

        return api_error(
            type="permission",
            message=(
                "У вас недостаточно "
                "прав для выполнения "
                "данного действия."
            ),
            status=403,
        )

    except Exception as e:

        return api_error(
            type="server_error",
            message=str(e),
            status=500,
        )