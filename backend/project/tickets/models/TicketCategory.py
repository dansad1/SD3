from django.db import models

from backend.generic.models import TimeStampedModel


class TicketCategory(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        "Описание",
        blank=True,
    )

    class Meta:

        ordering = [
            "name",
        ]

        verbose_name = "Категория заявки"
        verbose_name_plural = "Категории заявок"

    def __str__(self):

        return self.name
