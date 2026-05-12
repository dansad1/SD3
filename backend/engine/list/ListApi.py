# core/api/generics/ListApi.py

import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.list.ListRegistry import list_registry


@require_GET
def entity_list_api(request, entity: str):
    list_obj = list_registry.get(f"{entity}.list")
    result = list_obj.build(request)
    return JsonResponse(result)


class UserListSettings:
    pass


@require_GET
def entity_list_meta_api(request, entity):
    list_obj = list_registry.get(f"{entity}.list")

    fields = list_obj.get_fields(request)

    # entity-backed list
    try:
        entity_obj = entity_registry.get(entity)
        entity_obj.check_permission(request, "list")

        default_visible = (
                list_obj.get_default_visible_fields(request)
            or [f["key"] for f in fields]
        )

        settings = UserListSettings.objects.filter(
            user=request.user,
            entity=entity,
        ).first()

        if settings and settings.visible_fields:
            visible = settings.visible_fields
        else:
            visible = default_visible

        capabilities = entity_obj.get_capabilities_for_user(request)

    except KeyError:
        # resource-backed list
        list_obj.check_permission(request)
        visible = [f["key"] for f in fields]
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


@require_POST
def entity_list_settings_api(request, entity):
    data = json.loads(request.body or "{}")
    visible_fields = data.get("fields", [])

    entity_obj = entity_registry.get(entity)
    entity_obj.check_permission(request, "list")

    UserListSettings.objects.update_or_create(
        user=request.user,
        entity=entity,
        defaults={"visible_fields": visible_fields},
    )

    return JsonResponse({"status": "ok"})