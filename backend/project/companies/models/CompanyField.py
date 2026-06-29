from django.db import models

from backend.generic.models.BaseField import (
    BaseField,
)


class CompanyField(
    BaseField,
):

    fieldset = models.ForeignKey(
        "companies.CompanyFieldSet",
        on_delete=models.CASCADE,
        related_name="fields",
    )

    @property
    def value_model(self):
        from backend.project.companies.models import (
            CompanyFieldValue,
        )

        return CompanyFieldValue

    class Meta:

        unique_together = (
            "fieldset",
            "name",
        )

        verbose_name = (
            "Поле компании"
        )

        verbose_name_plural = (
            "Поля компании"
        )

    def __str__(self):

        return (
            f"{self.fieldset}: "
            f"{self.label}"
        )