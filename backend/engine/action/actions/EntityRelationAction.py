from django.core.exceptions import (
    ValidationError,
)

from rest_framework.generics import (
    get_object_or_404,
)

from backend.engine.action.Base.BaseAction import (
    BaseAction,
)

from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


class EntityRelationAction(
    BaseAction,
):

    code = "entity.relation"

    def run(
        self,
        request,
        payload,
        ctx,
    ):

        entity_name = ctx.get(
            "entity",
        )

        if not entity_name:
            return {
                "status": "error",
                "message": "Entity required",
            }

        entity = entity_registry.get(
            entity_name,
        )

        if not entity:
            return {
                "status": "error",
                "message": (
                    f"Entity '{entity_name}' not found"
                ),
            }

        entity.check_permission(
            request,
            "change",
        )

        object_id = ctx.get(
            "id",
        )

        if object_id is None:
            return {
                "status": "error",
                "message": "Object id required",
            }

        field_name = ctx.get(
            "field",
        )

        if not field_name:
            return {
                "status": "error",
                "message": "Relation field required",
            }

        operation = ctx.get(
            "operation",
            "add",
        )

        ids = (

            ctx.get(
                "ids",
            )

            or ctx.get(
                "selection",
                {},
            ).get(
                "ids",
                [],
            )

            or ctx.get(
                "extra",
                {},
            ).get(
                "ids",
                [],
            )

        )

        queryset = entity.get_queryset(
            request,
        )

        instance = get_object_or_404(
            queryset,
            pk=object_id,
        )

        relation = getattr(
            instance,
            field_name,
            None,
        )

        if relation is None:
            raise ValidationError(
                f"Relation '{field_name}' not found."
            )

        if not hasattr(
            relation,
            "add",
        ):
            raise ValidationError(
                f"'{field_name}' is not relation."
            )

        if operation == "clear":

            relation.clear()

        else:

            related_model = (
                relation.model
            )

            objects = list(
                related_model.objects.filter(
                    pk__in=ids,
                )
            )

            found = {
                obj.pk
                for obj in objects
            }

            missing = (
                set(ids)
                - found
            )

            if missing:
                raise ValidationError(
                    f"Objects not found: {sorted(missing)}"
                )

            if operation == "add":

                relation.add(
                    *objects,
                )

            elif operation == "remove":

                relation.remove(
                    *objects,
                )

            elif operation == "replace":

                relation.set(
                    objects,
                )

            else:

                return {
                    "status": "error",
                    "message": (
                        f"Unknown operation '{operation}'"
                    ),
                }

        return {

            "status": "ok",

            "effects": [

                {
                    "type": "table.reload",

                    "entity": entity_name,
                },

                {
                    "type": "toast",

                    "variant": "success",

                    "message": "Связь обновлена",
                },

            ],

        }