# backend/project/tickets/models/TicketAttachment.py

from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)


class TicketAttachment(TimeStampedModel):

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

    stored_file = models.ForeignKey(
        "generic.StoredFile",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="ticket_attachments",
    )

    uploaded_by = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="ticket_attachments",
    )

    class Meta:

        verbose_name = (
            "Вложение заявки"
        )

        verbose_name_plural = (
            "Вложения заявок"
        )

        ordering = [
            "-created_at",
        ]

    @property
    def file(self):
        return self.stored_file.file

    @property
    def original_name(self):
        return self.stored_file.original_name

    @property
    def mime_type(self):
        return self.stored_file.mime_type

    @property
    def size(self):
        return self.stored_file.size

    def __str__(self):

        return (
            self.original_name
            or f"Attachment #{self.pk}"
        )