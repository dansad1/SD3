# backend/project/tickets/actions/DeleteTicketCommentAction.py

from django.shortcuts import get_object_or_404

from backend.engine.action.Base.BaseAction import (
    BaseAction,
)

from backend.project.tickets.models import (
    TicketComment,
)

from backend.project.tickets.services.TicketCommentService import (
    TicketCommentService,
)


class DeleteTicketCommentAction(BaseAction):

    code = "ticket.delete_comment"

    permission = "ticket_comments.delete"

    confirm = "Удалить комментарий?"

    success_message = "Комментарий удалён."

    def execute(
        self,
        ctx,
    ):
        payload = ctx.payload or {}

        comment = get_object_or_404(
            TicketComment,
            pk=payload.get("id"),
        )

        ticket_id = comment.ticket_id

        TicketCommentService(
            ticket=comment.ticket,
            user=ctx.request.user,
        ).delete(
            comment
        )

        return {
            "deleted": True,
            "ticket": ticket_id,
        }