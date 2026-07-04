from django.views.decorators.http import require_GET

from backend.engine.entity.EntityRegistry import entity_registry


from django.views.decorators.http import require_GET

from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.import_export.excel.EntityExcelService import EntityExcelService


@require_GET
def entity_template_api(
    request,
    entity,
):
    entity = entity_registry.get(
        entity,
    )

    entity.check_permission(
        request,
        "view",
    )

    return (
        EntityExcelService(
            entity,
            request,
        )
        .template_response()
    )