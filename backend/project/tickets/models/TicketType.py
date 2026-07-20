from django.db import models

from backend.generic.models import TimeStampedModel


class TicketType(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=100,
    )

    code = models.SlugField(
        "Код",
        max_length=50,
        unique=True,
    )

    fieldset = models.ForeignKey(
        "tickets.TicketFieldSet",
        verbose_name="Набор полей",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="types",
    )

    class Meta:

        ordering = [
            "name",
        ]

        verbose_name = "Тип заявки"
        verbose_name_plural = "Типы заявок"

    def __str__(self):

        return self.name
