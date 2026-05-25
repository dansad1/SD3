from django.db import models

from backend.generic.models.BaseField import (
    BaseField,
)


class TicketField(
    BaseField
):

    fieldset = models.ForeignKey(
        "tickets.TicketFieldSet",
        on_delete=models.CASCADE,
        related_name="fields",
    )

    show_in_list = models.BooleanField(
        default=False,
    )

    default_expression = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:

        ordering = [
            "order",
            "id",
        ]

        unique_together = (
            "fieldset",
            "name",
        )

        verbose_name = (
            "Поле заявки"
        )

        verbose_name_plural = (
            "Поля заявки"
        )

    def __str__(self):

        return (
            f"{self.fieldset}: "
            f"{self.label}"
        )