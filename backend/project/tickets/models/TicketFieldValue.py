from decimal import Decimal

from django.db import models

from django.utils.dateparse import (
    parse_datetime,
)

from backend.generic.models.BaseFieldValue import (
    BaseFieldValue,
)


class TicketFieldValue(
    BaseFieldValue
):

    # =====================================================
    # RELATIONS
    # =====================================================

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "tickets.TicketField",
        on_delete=models.CASCADE,
        related_name="values",
    )

    # =====================================================
    # TYPED VALUES
    # =====================================================

    value_string = models.TextField(
        null=True,
        blank=True,
    )

    value_number = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
    )

    value_boolean = models.BooleanField(
        null=True,
        blank=True,
    )

    value_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    value_json = models.JSONField(
        null=True,
        blank=True,
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        unique_together = (
            "ticket",
            "field",
        )

        ordering = [
            "field",
            "id",
        ]

        indexes = [

            models.Index(
                fields=[
                    "ticket",
                    "field",
                ]
            ),

            models.Index(
                fields=[
                    "field",
                ]
            ),
        ]

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            f"{self.ticket} → "
            f"{self.field}"
        )

    # =====================================================
    # RUNTIME VALUE
    # =====================================================

    @property
    def value(self):

        field_type = (
            self.field.field_type
        )

        if field_type in [
            "string",
            "text",
            "richtext",
        ]:

            return self.value_string

        if field_type == "number":

            return self.value_number

        if field_type == "boolean":

            return self.value_boolean

        if field_type in [
            "date",
            "datetime",
        ]:

            return self.value_datetime

        if field_type == "json":

            return self.value_json

        return self.value_string

    # =====================================================
    # VALUE SETTER
    # =====================================================

    @value.setter
    def value(
        self,
        value,
    ):

        field_type = (
            self.field.field_type
        )

        # reset

        self.value_string = None
        self.value_number = None
        self.value_boolean = None
        self.value_datetime = None
        self.value_json = None

        # strings

        if field_type in [
            "string",
            "text",
            "richtext",
        ]:

            self.value_string = value

        # number

        elif field_type == "number":

            if value is not None:

                self.value_number = Decimal(
                    str(value)
                )

        # boolean

        elif field_type == "boolean":

            self.value_boolean = bool(
                value
            )

        # datetime

        elif field_type in [
            "date",
            "datetime",
        ]:

            if isinstance(
                value,
                str,
            ):

                value = parse_datetime(
                    value
                )

            self.value_datetime = value

        # json

        elif field_type == "json":

            self.value_json = value