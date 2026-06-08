# backend/project/tickets/actions/DeleteTicketAttachmentAction.py

from django.shortcuts import get_object_or_404

from backend.engine.action.Base.BaseAction import (
    BaseAction,
)

from backend.project.tickets.models import (
    TicketAttachment,
)

from backend.project.tickets.services.TicketAttachmentService import (
    TicketAttachmentService,
)

from backend.project.tickets.services.TicketNotificationService import (
    TicketNotificationService,
)


class DeleteTicketAttachmentAction(BaseAction):

    code = "ticket.delete_attachment"

    permission = "ticket_attachments.delete"

    confirm = "Удалить файл?"

    success_message = "Файл удалён."

    def execute(
        self,
        ctx,
    ):
        payload = ctx.payload or {}

        attachment = get_object_or_404(
            TicketAttachment,
            pk=payload.get("id"),
        )

        ticket = attachment.ticket
        attachment_id = attachment.id

        TicketAttachmentService(
            ticket=ticket,
            user=ctx.request.user,
        ).delete(
            attachment
        )

        TicketNotificationService.attachment_deleted(
            ticket=ticket,
            attachment_id=attachment_id,
            user=ctx.request.user,
        )

        return {
            "deleted": True,
            "ticket": ticket.id,
        }