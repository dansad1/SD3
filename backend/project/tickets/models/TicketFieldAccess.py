from django.db import models

from backend.generic.models.BaseFieldAccess import (
    BaseFieldAccess,
)


class TicketFieldAccess(
    BaseFieldAccess,
):

    field = models.ForeignKey(
        "tickets.TicketField",
        verbose_name="Поле заявки",
        on_delete=models.CASCADE,
        related_name="accesses",
    )

    class Meta(
        BaseFieldAccess.Meta,
    ):

        unique_together = (
            "field",
            "role",
        )

        verbose_name = "Доступ к полю заявки"
        verbose_name_plural = "Доступы к полям заявки"
