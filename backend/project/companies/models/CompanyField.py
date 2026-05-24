from django.db import models

from backend.generic.models import (
    BaseField,
)


class CompanyField(
    BaseField
):

    fieldset = models.ForeignKey(
        "companies.CompanyFieldSet",
        on_delete=models.CASCADE,
        related_name="fields",
    )

    class Meta:

        ordering = [
            "order",
            "id",
        ]

        unique_together = (
            "fieldset",
            "name",
        )

    def __str__(self):

        return (
            f"{self.fieldset}: "
            f"{self.label}"
        )