from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)
from backend.generic.models.DynamicModelMixin import (
    DynamicModelMixin,
)


class Company(
    DynamicModelMixin,
    TimeStampedModel,
):

    fieldset = models.ForeignKey(
        "companies.CompanyFieldSet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="companies",
    )

    archived = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = [
            "-id",
        ]

    def __str__(
        self,
    ):
        return (
            self.get_value(
                "name",
            )
            or f"Company #{self.pk}"
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
            self.fieldset.fields
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