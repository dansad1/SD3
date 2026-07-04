from django.views.decorators.http import require_GET

from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.import_export.excel import EntityExcelService


@require_GET
def entity_export_api(
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
        .export_response()
    )
