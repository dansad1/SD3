from django.db import models

from backend.generic.models import TimeStampedModel


class TicketSLA(TimeStampedModel):

    type = models.ForeignKey(
        "tickets.TicketType",
        verbose_name="Тип заявки",
        on_delete=models.CASCADE,
        related_name="slas",
    )

    priority = models.ForeignKey(
        "tickets.TicketPriority",
        verbose_name="Приоритет",
        on_delete=models.CASCADE,
        related_name="slas",
    )

    hours = models.PositiveIntegerField(
        "Срок выполнения, часов",
        default=0,
    )

    class Meta:

        unique_together = (
            "type",
            "priority",
        )

        ordering = [
            "type",
            "priority",
        ]

        verbose_name = "SLA заявки"
        verbose_name_plural = "SLA заявок"

    def __str__(self):

        return (
            f"{self.type} / "
            f"{self.priority} — "
            f"{self.hours} ч."
        )
