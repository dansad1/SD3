from rest_framework.generics import get_object_or_404

from backend.engine.action.Base.BaseAction import BaseAction
from backend.engine.entity.EntityRegistry import entity_registry


class EntityDeleteAction(BaseAction):

    code = "entity.delete"

    def run(self, request, payload, ctx):

        entity = ctx.get("entity")
        row = ctx.get("row")

        if not entity or not row:
            return {"status": "error", "message": "Invalid ctx"}

        entity_obj = entity_registry.get(entity)

        entity_obj.check_permission(request, "delete")

        instance = get_object_or_404(
            entity_obj.get_queryset(request),
            pk=row.get("id")
        )

        entity_obj.delete_instance(request, instance)

        return {
            "status": "ok",
            "effects": [
                {"type": "table.reload", "entity": entity},
                {"type": "toast", "variant": "success"}
            ]
        }


