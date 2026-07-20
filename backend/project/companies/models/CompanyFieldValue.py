from django.db import models

from backend.generic.models import BaseFieldValue


class CompanyFieldValue(BaseFieldValue):

    company = models.ForeignKey(
        "companies.Company",
        verbose_name="Компания",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "companies.CompanyField",
        verbose_name="Поле компании",
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

        verbose_name = "Значение поля компании"
        verbose_name_plural = "Значения полей компаний"

    def __str__(self):

        return (
            f"{self.company} → "
            f"{self.field}"
        )
