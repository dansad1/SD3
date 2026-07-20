from django.db import models

from backend.generic.models import (
    DynamicField,
    TimeStampedModel,
)
from backend.generic.models.DynamicModelMixin import (
    DynamicModelMixin,
)


class Ticket(
    DynamicModelMixin,
    TimeStampedModel,
):

    type = models.ForeignKey(
        "tickets.TicketType",
        verbose_name="Тип заявки",
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    archived = models.BooleanField(
        "Архивирована",
        default=False,
    )

    class Meta:

        ordering = [
            "-id",
        ]

        indexes = [
            models.Index(
                fields=[
                    "type",
                ],
            ),
            models.Index(
                fields=[
                    "created_at",
                ],
            ),
        ]

        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(
        self,
    ):

        return (
            self.get_value(
                "name",
            )
            or f"Ticket #{self.pk}"
        )

    def set_value(
        self,
        field_name,
        value,
    ):

        if not self.type_id:

            raise ValueError(
                "Тип заявки не указан."
            )

        source = (
            self.type.fieldset.fields
            .filter(
                name=field_name,
            )
            .first()
        )

        if source is None:

            raise ValueError(
                f"Неизвестное поле: {field_name}"
            )

        DynamicField(
            source,
        ).set_value(
            self,
            value,
        )
