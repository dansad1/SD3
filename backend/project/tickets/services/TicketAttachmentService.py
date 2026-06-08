# backend/project/tickets/services/TicketAttachmentService.py

from django.core.exceptions import PermissionDenied

from backend.project.tickets.models import (
    TicketAttachment,
)


class TicketAttachmentService:

    def __init__(
        self,
        ticket,
        user,
    ):
        self.ticket = ticket
        self.user = user

    def create(
        self,
        file,
        field=None,
    ):
        if not self.user.has_perm(
            "tickets.ticket_attachments.create"
        ):
            raise PermissionDenied

        return TicketAttachment.objects.create(
            ticket=self.ticket,
            field=field,
            file=file,
            original_name=getattr(
                file,
                "name",
                "",
            ),
            mime_type=getattr(
                file,
                "content_type",
                "",
            ),
            size=getattr(
                file,
                "size",
                0,
            ),
            uploaded_by=self.user,
        )

    def delete(
        self,
        attachment,
    ):
        if not self.can_delete(attachment):
            raise PermissionDenied

        if attachment.file:
            attachment.file.delete(
                save=False,
            )

        attachment.delete()

    def can_delete(
        self,
        attachment,
    ):
        if self.user.is_superuser:
            return True

        if self.user.has_perm(
            "tickets.ticket_attachments.delete"
        ):
            return True

        return attachment.uploaded_by_id == self.user.id