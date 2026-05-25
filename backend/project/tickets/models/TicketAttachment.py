import uuid

from django.db import models


def ticket_attachment_upload_path(
    instance,
    filename,
):

    ext = (
        filename.split(".")[-1]
        if "." in filename
        else ""
    )

    generated = uuid.uuid4().hex

    if ext:
        generated = (
            f"{generated}.{ext}"
        )

    return (
        f"tickets/"
        f"{instance.ticket_id}/"
        f"{generated}"
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
        upload_to=(
            ticket_attachment_upload_path
        )
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

        ordering = [
            "-created_at",
        ]

        indexes = [

            models.Index(
                fields=[
                    "ticket",
                ]
            ),
        ]

        verbose_name = (
            "Вложение заявки"
        )

        verbose_name_plural = (
            "Вложения заявок"
        )

    def __str__(self):

        return (
            self.original_name
            or f"Attachment #{self.pk}"
        )