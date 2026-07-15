from django.db import models

from backend.generic.models.BaseFieldAccess import (
    BaseFieldAccess,
)


class TicketFieldAccess(
    BaseFieldAccess,
):

    field = models.ForeignKey(
        "tickets.TicketField",
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