from django.db import models

from backend.generic.models import (
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
    # DYNAMIC VALUES
    # =====================================================

    def get_dynamic_map(
        self,
    ):

        if hasattr(
            self,
            "_dynamic_map",
        ):
            return self._dynamic_map

        values = {}

        for item in (
            self.dynamic_values
            .select_related(
                "field",
            )
            .all()
        ):

            values[
                item.field.name
            ] = item.value

        self._dynamic_map = values

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
            self.get_dynamic_map()
            .get(
                field_name,
                default,
            )
        )

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

        if hasattr(
            self,
            "_dynamic_map",
        ):

            delattr(
                self,
                "_dynamic_map",
            )