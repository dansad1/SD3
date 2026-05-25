# backend/project/tickets/models/TicketAttachment.py

from django.db import models

from backend.project.tickets.utils.upload_paths import (
    ticket_attachment_upload_path,
)


class TicketAttachment(models.Model):

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    field = models.ForeignKey(
        "tickets.TicketField",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="attachments",
    )

    uploaded_by = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="ticket_attachments",
    )

    file = models.FileField(
        upload_to=ticket_attachment_upload_path,
    )

    original_name = models.CharField(
        max_length=255,
    )

    mime_type = models.CharField(
        max_length=255,
        blank=True,
    )

    size = models.BigIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = (
            "Вложение заявки"
        )

        verbose_name_plural = (
            "Вложения заявок"
        )

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return (
            self.original_name
            or f"Attachment #{self.pk}"
        )