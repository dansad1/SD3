from django.db import models

from backend.generic.models import BaseFieldValue


class CompanyFieldValue(BaseFieldValue):

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "companies.CompanyField",
        on_delete=models.CASCADE,
        related_name="values",
    )

    class Meta:

        unique_together = (
            "company",
            "field",
        )

        indexes = [

            models.Index(
                fields=[
                    "company",
                    "field",
                ],
            ),

            models.Index(
                fields=[
                    "field",
                ],
            ),
        ]

    def __str__(self):

        return (
            f"{self.company} → "
            f"{self.field}"
        )