from backend.project.audit.resources.EntityHistoryResource import (
    EntityHistoryResource,
)

from backend.project.tickets.models import (
    Ticket,
    TicketAttachment,
    TicketComment,
)


class TicketHistoryResource(
    EntityHistoryResource,
):

    code = "ticket.history"

    ENTITY = "tickets"

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

        ticket = (
            Ticket.objects
            .filter(
                pk=ticket_id,
            )
            .first()
        )

        if not ticket:
            return []

        events = []

        # =====================================================
        # CREATE
        # =====================================================

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

            "object_repr":
                str(ticket),

            "changes":
                {},

            "meta": {

                "title":
                    "Заявка создана",

                "text":
                    "Заявка была создана.",

            },

        })

        # =====================================================
        # AUDIT
        # =====================================================

        events.extend(

            self.get_history(

                request=request,

                entity=self.ENTITY,

                object_id=ticket.pk,

            )

        )

        # =====================================================
        # COMMENTS
        # =====================================================

        comments = (

            TicketComment.objects

            .filter(
                ticket=ticket,
            )

            .select_related(
                "author",
                "edited_by",
            )

            .order_by(
                "-created_at",
            )

        )

        for item in comments:

            can_manage = (

                request.user.is_authenticated

                and (

                    request.user.is_superuser

                    or item.author_id == request.user.pk

                )

            )

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
                    (
                        {
                            "id":
                                item.author_id,

                            "label":
                                str(item.author),

                        }
                        if item.author
                        else None
                    ),

                "object_repr":
                    None,

                "changes":
                    {},

                "meta": {

                    "id":
                        item.pk,

                    "title":
                        "Комментарий",

                    "text":
                        item.text,

                    "hidden":
                        item.hide_from_client,

                    "edited":
                        bool(
                            item.edited_at,
                        ),

                    "edited_at":
                        (
                            item.edited_at.isoformat()
                            if item.edited_at
                            else None
                        ),

                    "edited_by":
                        (
                            str(
                                item.edited_by,
                            )
                            if item.edited_by
                            else None
                        ),

                    "can_edit":
                        can_manage,

                    "can_delete":
                        can_manage,

                },

            })

        # =====================================================
        # ATTACHMENTS
        # =====================================================

        attachments = (

            TicketAttachment.objects

            .filter(
                ticket=ticket,
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
                    (
                        {
                            "id":
                                item.uploaded_by_id,

                            "label":
                                str(item.uploaded_by),

                        }
                        if item.uploaded_by
                        else None
                    ),

                "object_repr":
                    None,

                "changes":
                    {},

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

        # =====================================================
        # SORT
        # =====================================================

        events.sort(

            key=lambda event:
                event["created"],

            reverse=True,

        )

        return events