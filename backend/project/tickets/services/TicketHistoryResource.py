from backend.engine.Resource.BaseResource import (
    BaseResource,
)

from backend.project.audit.models.EntityJournal import (
    EntityJournal,
)

from backend.project.tickets.models import (
    Ticket,
    TicketAttachment,
    TicketComment,
)


class TicketHistoryResource(
    BaseResource,
):

    code = "ticket.history"

    def get(
        self,
        request,
        **params,
    ):

        ticket_id = params.get(
            "id",
        )

        if not ticket_id:
            return []

        events = []

        ticket = (
            Ticket.objects
            .filter(
                pk=ticket_id,
            )
            .first()
        )

        if ticket:

            events.append({

                "id":
                    f"ticket-{ticket.pk}",

                "type":
                    "create",

                "action":
                    "create",

                "created":
                    ticket.created_at.isoformat(),

                "actor":
                    None,

                "meta": {

                    "title":
                        "Заявка создана",

                },

            })

        journal = (

            EntityJournal.objects

            .filter(
                entity="tickets",
                object_id=str(
                    ticket_id,
                ),
            )

            .select_related(
                "actor",
            )

            .order_by(
                "-created",
            )

        )

        for item in journal:

            changes = (
                item.changes
                or {}
            )

            event_type = (
                "field_changes"
            )

            if (
                len(changes) == 1
            ):

                field = next(
                    iter(changes)
                )

                if field == "status":
                    event_type = "status"

                elif field in {
                    "executor",
                    "assignee",
                }:
                    event_type = "assign"

            events.append({

                "id":
                    f"audit-{item.pk}",

                "type":
                    event_type,

                "action":
                    event_type,

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

                "changes":
                    changes,

                "meta":
                    item.meta,

            })

        comments = (

            TicketComment.objects

            .filter(
                ticket_id=ticket_id,
            )

            .select_related(
                "author",
            )

            .order_by(
                "-created_at",
            )

        )

        for item in comments:

            events.append({

                "id":
                    f"comment-{item.pk}",

                "type":
                    "comment",

                "action":
                    "comment",

                "created":
                    item.created_at.isoformat(),

                "actor":
                    {
                        "id":
                            item.author_id,

                        "label":
                            str(item.author),
                    }
                    if item.author
                    else None,

                "meta": {

                    "text":
                        item.text,

                },

            })

        attachments = (

            TicketAttachment.objects

            .filter(
                ticket_id=ticket_id,
            )

            .select_related(
                "uploaded_by",
            )

            .order_by(
                "-created_at",
            )

        )

        for item in attachments:

            events.append({

                "id":
                    f"attachment-{item.pk}",

                "type":
                    "attachment",

                "action":
                    "attachment",

                "created":
                    item.created_at.isoformat(),

                "actor":
                    {
                        "id":
                            item.uploaded_by_id,

                        "label":
                            str(
                                item.uploaded_by
                            ),
                    }
                    if item.uploaded_by
                    else None,

                "meta": {

                    "title":
                        "Добавлено вложение",

                    "text":
                        item.original_name,

                    "size":
                        item.size,

                    "mime_type":
                        item.mime_type,

                },

            })

        events.sort(

            key=lambda item:
                item["created"],

            reverse=True,

        )

        return events