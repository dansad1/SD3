# backend/project/audit/resources/EntityHistoryResource.py

from backend.engine.Resource.BaseResource import BaseResource

from backend.project.audit.models.EntityJournal import (
    EntityJournal,
)


class EntityHistoryResource(BaseResource):

    code = "entity.history"

    def get(
        self,
        request,
        **params,
    ):

        entity = params.get(
            "entity"
        )

        object_id = params.get(
            "id"
        )

        if (
            not entity
            or not object_id
        ):
            return []

        qs = (
            EntityJournal.objects
            .filter(
                entity=entity,
                object_id=str(
                    object_id
                ),
            )
            .select_related(
                "actor"
            )
            .order_by(
                "-created"
            )
        )

        return [

            {
                "id":
                    item.pk,

                "action":
                    item.action,

                "created":
                    item.created.isoformat(),

                "actor":
                    {
                        "id":
                            item.actor_id,

                        "label":
                            str(item.actor),
                    }
                    if item.actor
                    else None,

                "object_repr":
                    item.object_repr,

                "changes":
                    item.changes,

                "meta":
                    item.meta,
            }

            for item in qs

        ]