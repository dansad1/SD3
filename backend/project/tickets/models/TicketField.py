from django.db import models

from backend.generic.models.BaseField import (
    BaseField,
)


class TicketField(
    BaseField,
):

    fieldset = models.ForeignKey(
        "tickets.TicketFieldSet",
        on_delete=models.CASCADE,
        related_name="fields",
    )

    @property
    def value_model(self):
        from backend.project.tickets.models import (
            TicketFieldValue,
        )

        return TicketFieldValue

    class Meta:

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