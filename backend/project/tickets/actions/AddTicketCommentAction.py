# backend/project/tickets/actions/AddTicketCommentAction.py

from django.shortcuts import get_object_or_404

from backend.engine.action.Base.BaseAction import (
    BaseAction,
)

from backend.project.tickets.models import (
    Ticket,
)

from backend.project.tickets.services.TicketCommentService import (
    TicketCommentService,
)

from backend.project.tickets.services.TicketNotificationService import (
    TicketNotificationService,
)


class AddTicketCommentAction(BaseAction):

    code = "ticket.add_comment"

    permission = "ticket_comments.create"

    success_message = "Комментарий добавлен."

    def execute(
        self,
        ctx,
    ):
        payload = ctx.payload or {}

        ticket = get_object_or_404(
            Ticket,
            pk=payload.get("ticket"),
        )

        comment = TicketCommentService(
            ticket=ticket,
            user=ctx.request.user,
        ).create(
            text=payload.get("text"),
            hide_from_client=payload.get(
                "hide_from_client",
                False,
            ),
        )

        TicketNotificationService.comment_added(
            ticket=ticket,
            comment=comment,
            user=ctx.request.user,
        )

        return {
            "id": comment.id,
            "ticket": ticket.id,
        }