from django.db import models

from backend.generic.models import BaseFieldValue


class TicketFieldValue(BaseFieldValue):

    ticket = models.ForeignKey(
        "tickets.Ticket",
        verbose_name="Заявка",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "tickets.TicketField",
        verbose_name="Поле заявки",
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

        verbose_name = "Значение поля заявки"
        verbose_name_plural = "Значения полей заявок"

    def __str__(self):

        return (
            f"{self.ticket} → "
            f"{self.field}"
        )
