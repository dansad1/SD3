from backend.engine.Resource.BaseResource import (
    BaseResource,
)

from backend.project.audit.models import (
    EntityJournal,
)


class TicketHistoryResource(BaseResource):

    code = "ticket.history"

    def get(
        self,
        request,
        **params,
    ):

        ticket_id = params.get("id")

        if not ticket_id:
            return []

        events = []

        # =================================================
        # AUDIT
        # =================================================

        journal = (
            EntityJournal.objects
            .filter(
                entity="ticket",
                object_id=str(ticket_id),
            )
            .select_related("actor")
            .order_by("-created")
        )

        for item in journal:

            events.append({

                "id": f"audit-{item.pk}",

                "type": "change",

                "action": item.action,

                "created": item.created.isoformat(),

                "actor": (
                    {
                        "id": item.actor_id,
                        "label": str(item.actor),
                    }
                    if item.actor
                    else None
                ),

                "changes": item.changes,
            })

        # =================================================
        # COMMENTS
        # =================================================

        # TicketComment.objects...

        # =================================================
        # ATTACHMENTS
        # =================================================

        # TicketAttachment.objects...

        # =================================================
        # SORT
        # =================================================

        events.sort(
            key=lambda x: x["created"],
            reverse=True,
        )

        return events