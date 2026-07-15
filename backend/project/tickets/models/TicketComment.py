from django.conf import settings
from django.db import models

from backend.generic.models import TimeStampedModel


from django.conf import settings
from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)


class TicketComment(
    TimeStampedModel,
):

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_comments",
    )

    text = models.TextField()

    hide_from_client = models.BooleanField(
        default=False,
    )

    edited_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:

        verbose_name = (
            "Комментарий заявки"
        )

        verbose_name_plural = (
            "Комментарии заявок"
        )

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return (
            f"Комментарий #{self.pk}"
        )