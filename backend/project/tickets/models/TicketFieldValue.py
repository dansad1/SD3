from django.db import models

from backend.generic.models import BaseFieldValue


class TicketFieldValue(BaseFieldValue):

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "tickets.TicketField",
        on_delete=models.CASCADE,
        related_name="values",
    )

    class Meta:

        unique_together = (
            "ticket",
            "field",
        )

        ordering = [
            "field",
            "id",
        ]

        indexes = [

            models.Index(
                fields=[
                    "ticket",
                    "field",
                ],
            ),

            models.Index(
                fields=[
                    "field",
                ],
            ),
        ]

    def __str__(self):

        return (
            f"{self.ticket} → "
            f"{self.field}"
        )