# backend/project/tickets/actions/UploadTicketAttachmentAction.py

from django.shortcuts import get_object_or_404

from backend.engine.action.Base.BaseAction import (
    BaseAction,
)

from backend.project.tickets.models import (
    Ticket,
    TicketField,
)

from backend.project.tickets.services.TicketAttachmentService import (
    TicketAttachmentService,
)

from backend.project.tickets.services.TicketNotificationService import (
    TicketNotificationService,
)


class UploadTicketAttachmentAction(BaseAction):

    code = "ticket.upload_attachment"

    permission = "ticket_attachments.create"

    success_message = "Файл загружен."

    def execute(
        self,
        ctx,
    ):
        payload = ctx.payload or {}

        ticket = get_object_or_404(
            Ticket,
            pk=payload.get("ticket"),
        )

        file = (
            ctx.request.FILES.get("file")
            if hasattr(ctx.request, "FILES")
            else None
        )

        if not file:
            raise ValueError(
                "Файл не передан."
            )

        field = None

        field_id = payload.get("field")

        if field_id:
            field = get_object_or_404(
                TicketField,
                pk=field_id,
            )

        attachment = TicketAttachmentService(
            ticket=ticket,
            user=ctx.request.user,
        ).create(
            file=file,
            field=field,
        )

        TicketNotificationService.attachment_added(
            ticket=ticket,
            attachment=attachment,
            user=ctx.request.user,
        )

        return {
            "id": attachment.id,
            "ticket": ticket.id,
            "name": attachment.original_name,
        }