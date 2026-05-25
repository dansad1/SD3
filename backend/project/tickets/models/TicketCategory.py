from django.db import models


class TicketCategory(models.Model):

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