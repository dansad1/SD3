from django.conf import settings
from django.db import models


class Ticket(models.Model):

    # =====================================================
    # SCHEMA
    # =====================================================

    type = models.ForeignKey(
        "tickets.TicketType",
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    # =====================================================
    # AUDIT
    # =====================================================

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_tickets",
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets",
    )

    # =====================================================
    # SYSTEM
    # =====================================================

    archived = models.BooleanField(
        default=False,
    )

    # =====================================================
    # DATES
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
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
                ]
            ),

            models.Index(
                fields=[
                    "assigned_to",
                ]
            ),

            models.Index(
                fields=[
                    "created_at",
                ]
            ),
        ]

        verbose_name = (
            "Заявка"
        )

        verbose_name_plural = (
            "Заявки"
        )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            self.get_value("title")
            or f"Ticket #{self.pk}"
        )

    # =====================================================
    # DYNAMIC VALUES CACHE
    # =====================================================

    def get_dynamic_values_map(self):

        if not hasattr(
            self,
            "_dynamic_values_map",
        ):

            self._dynamic_values_map = {

                value.field.name: value

                for value in (
                    self.dynamic_values
                    .select_related("field")
                    .all()
                )
            }

        return (
            self._dynamic_values_map
        )

    # =====================================================
    # GET VALUE
    # =====================================================

    def get_value(
        self,
        field_name,
        default=None,
    ):

        value = (
            self.get_dynamic_values_map()
            .get(field_name)
        )

        if not value:
            return default

        return value.value