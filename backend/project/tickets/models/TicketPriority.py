from django.db import models

from backend.generic.models import TimeStampedModel


class TicketPriority(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=100,
    )

    level = models.PositiveIntegerField(
        "Уровень",
        help_text=(
            "Чем меньше число — "
            "тем выше приоритет"
        ),
    )

    color = models.CharField(
        "Цвет",
        max_length=7,
        default="#cccccc",
    )

    class Meta:

        ordering = [
            "level",
        ]

        verbose_name = "Приоритет заявки"
        verbose_name_plural = "Приоритеты заявок"

    def __str__(self):

        return self.name
