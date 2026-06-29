from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericRelation,
)
from django.db import models

from backend.generic.models import (
    DynamicValue,
    TimeStampedModel,
)


class Ticket(TimeStampedModel):

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

    dynamic_values = GenericRelation(
        DynamicValue,
        content_type_field="content_type",
        object_id_field="object_id",
        related_query_name="ticket",
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

    def __str__(self):

        return (
            self.get_value("title")
            or f"Ticket #{self.pk}"
        )

    # =====================================================
    # DYNAMIC CACHE
    # =====================================================

    def get_dynamic_values_map(
        self,
    ):

        if hasattr(
            self,
            "_dynamic_values_map",
        ):
            return self._dynamic_values_map

        values = {}

        for item in self.dynamic_values.all():

            values[
                item.field_name
            ] = item.value

        self._dynamic_values_map = values

        return values

    # =====================================================
    # VALUE
    # =====================================================

    def get_value(
        self,
        field_name,
        default=None,
    ):

        return (
            self.get_dynamic_values_map()
            .get(
                field_name,
                default,
            )
        )