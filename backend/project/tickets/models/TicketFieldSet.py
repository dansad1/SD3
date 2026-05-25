from backend.generic.models.BaseFieldSet import (
    BaseFieldSet,
)


class TicketFieldSet(
    BaseFieldSet
):

    class Meta:

        ordering = [
            "order",
            "id",
        ]

        verbose_name = (
            "Набор полей заявки"
        )

        verbose_name_plural = (
            "Наборы полей заявки"
        )

    def __str__(self):

        return self.name