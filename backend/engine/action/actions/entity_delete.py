from rest_framework.generics import (
    get_object_or_404,
)

from backend.engine.action.Base.BaseAction import (
    BaseAction,
)
from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


class EntityDeleteAction(BaseAction):

    code = "entity.delete"

    def run(self, request, payload, ctx):

        entity = ctx.get("entity")

        if not entity:
            return {
                "status": "error",
                "message": "Entity required",
            }

        entity_obj = entity_registry.get(entity)

        entity_obj.check_permission(
            request,
            "delete",
        )

        ids = (
            ctx.get(
                "selection",
                {},
            ).get(
                "ids",
                [],
            )
            or ctx.get(
                "ids",
                [],
            )
        )

        if not ids:

            row = ctx.get(
                "row",
                {},
            )

            pk = row.get("id")

            if pk is not None:
                ids = [pk]

        if not ids:
            return {
                "status": "error",
                "message": "Nothing selected",
            }

        qs = entity_obj.get_queryset(
            request,
        )

        deleted = 0

        for pk in ids:

            instance = get_object_or_404(
                qs,
                pk=pk,
            )

            entity_obj.delete_instance(
                request,
                instance,
            )

            deleted += 1

        return {
            "status": "ok",

            "effects": [

                {
                    "type": "table.reload",
                    "entity": entity,
                },

                {
                    "type": "toast",
                    "variant": "success",
                    "message": (
                        f"Удалено: {deleted}"
                    ),
                },

            ],
        }