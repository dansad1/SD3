from django.db import models

from backend.generic.models import TimeStampedModel


class TicketCategory(TimeStampedModel):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = [
            "name",
        ]

    def __str__(self):

        return self.name