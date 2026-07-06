from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)
from backend.generic.models.DynamicModelMixin import (
    DynamicModelMixin,
)


class Ticket(
    DynamicModelMixin,
    TimeStampedModel,
):

    # =====================================================
    # SCHEMA
    # =====================================================

    type = models.ForeignKey(
        "tickets.TicketType",
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    # =====================================================
    # SYSTEM
    # =====================================================

    archived = models.BooleanField(
        default=False,
    )

    # =====================================================
    # META
    # =====================================================

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

    # =====================================================
    # STRING
    # =====================================================

    def __str__(
        self,
    ):
        return (
            self.get_value(
                "title",
            )
            or f"Ticket #{self.pk}"
        )

    # =====================================================
    # VALUE
    # =====================================================

    def set_value(
        self,
        field_name,
        value,
    ):

        field = (
            self.type.fieldset.fields
            .filter(
                name=field_name,
            )
            .first()
        )

        if field is None:
            raise ValueError(
                f"Unknown field: {field_name}"
            )

        field.set_value(
            self,
            value,
        )

        self.invalidate_dynamic_cache()