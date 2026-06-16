from django.conf import settings
from django.db import models

from backend.generic.models import TimeStampedModel


class TicketComment(TimeStampedModel):

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




    class Meta:
        verbose_name = (
            "Комментарий заявки"
        )

        verbose_name_plural = (
            "Комментарии заявок"
        )

    def __str__(self):

        return (
            f"Комментарий "
            f"#{self.pk}"
        )