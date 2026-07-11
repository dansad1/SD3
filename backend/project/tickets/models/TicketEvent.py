from django.db import models

from backend import settings


class TicketEvent(models.Model):
    EVENT_CHANGE = "change"
    EVENT_COMMENT = "comment"

    EVENT_TYPES = [
        (EVENT_CHANGE, "Изменение"),
        (EVENT_COMMENT, "Комментарий"),
    ]

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="events",
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        db_index=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )

    data = models.JSONField(
        default=dict,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )