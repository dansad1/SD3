from django.db import models

from backend.generic.models.BaseFieldAccess import (
    BaseFieldAccess,
)


class CompanyFieldAccess(
    BaseFieldAccess,
):

    field = models.ForeignKey(
        "companies.CompanyField",
        verbose_name="Поле компании",
        on_delete=models.CASCADE,
        related_name="accesses",
    )

    class Meta(
        BaseFieldAccess.Meta,
    ):

        unique_together = (
            "field",
            "role",
        )

        verbose_name = "Доступ к полю компании"
        verbose_name_plural = "Доступы к полям компании"
