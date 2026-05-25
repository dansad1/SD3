from django.db import models


class TicketPriority(models.Model):

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