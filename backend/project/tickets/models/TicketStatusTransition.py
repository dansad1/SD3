from django.db import models

from backend.generic.models import TimeStampedModel


class TicketStatusTransition(TimeStampedModel):

    source = models.ForeignKey(
        "tickets.TicketStatus",
        verbose_name="Исходный статус",
        on_delete=models.CASCADE,
        related_name="transitions_from",
    )

    target = models.ForeignKey(
        "tickets.TicketStatus",
        verbose_name="Целевой статус",
        on_delete=models.CASCADE,
        related_name="transitions_to",
    )

    allowed_roles = models.ManyToManyField(
        "users.UserRole",
        verbose_name="Разрешённые роли",
        blank=True,
        related_name="ticket_transitions",
    )

    class Meta:

        unique_together = (
            "source",
            "target",
        )

        ordering = [
            "source",
            "target",
        ]

        verbose_name = "Переход статуса заявки"
        verbose_name_plural = "Переходы статусов заявок"

    def __str__(self):

        return (
            f"{self.source} → "
            f"{self.target}"
        )
