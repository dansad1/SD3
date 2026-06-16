from django.db import models

from backend.generic.models import TimeStampedModel


class TicketPriority(TimeStampedModel):

    name = models.CharField(
        max_length=100,
    )

    level = models.PositiveIntegerField(
        help_text=(
            "Чем меньше число — "
            "тем выше приоритет"
        )
    )

    color = models.CharField(
        max_length=7,
        default="#cccccc",
    )

    class Meta:

        ordering = [
            "level",
        ]

    def __str__(self):

        return self.name