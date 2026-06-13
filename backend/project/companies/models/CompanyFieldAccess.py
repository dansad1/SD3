from django.db import models

from backend.generic.models.BaseFieldAccess import (
    BaseFieldAccess,
)


class CompanyFieldAccess(BaseFieldAccess):

    field = models.ForeignKey(
        "companies.CompanyField",
        on_delete=models.CASCADE,
        related_name="accesses",
    )

    class Meta:

        unique_together = (
            "field",
            "role",
        )

        ordering = [
            "field",
            "role",
        ]

        indexes = [

            models.Index(
                fields=[
                    "field",
                    "role",
                ]
            ),

            models.Index(
                fields=[
                    "role",
                ]
            ),
        ]

        verbose_name = (
            "Company field access"
        )

        verbose_name_plural = (
            "Company field accesses"
        )

    def __str__(self):

        return (
            f"{self.role} → "
            f"{self.field} "
            f"({self.access_level})"
        )