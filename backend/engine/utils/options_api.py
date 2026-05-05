from django.http import JsonResponse
from django.views.decorators.http import require_GET

from SD3.backend.engine.entity.EntityRegistry import entity_registry


@require_GET
def entity_options_api(request, entity: str):

    ent = entity_registry.get(entity)

    ent.check_permission(request, "list")

    items = ent.get_options(request)

    return JsonResponse({
        "items": items
    })