from django.db import models

from backend.project.users.models import (
    UserRole,
)


class CompanyFieldAccess(models.Model):

    ACCESS_NONE = "none"

    ACCESS_VIEW = "view"

    ACCESS_EDIT = "edit"

    ACCESS_CHOICES = [

        (
            ACCESS_NONE,
            "Нет доступа",
        ),

        (
            ACCESS_VIEW,
            "Просмотр",
        ),

        (
            ACCESS_EDIT,
            "Редактирование",
        ),
    ]

    # =====================================================
    # RELATIONS
    # =====================================================

    field = models.ForeignKey(

        "companies.CompanyField",

        on_delete=models.CASCADE,

        related_name="accesses",
    )

    role = models.ForeignKey(

        UserRole,

        on_delete=models.CASCADE,

        related_name="company_field_accesses",
    )

    # =====================================================
    # ACCESS
    # =====================================================

    access_level = models.CharField(

        max_length=16,

        choices=ACCESS_CHOICES,

        default=ACCESS_NONE,
    )

    # =====================================================
    # META
    # =====================================================

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

    # =====================================================
    # STR
    # =====================================================

    def __str__(self):

        return (
            f"{self.role} → "
            f"{self.field} "
            f"({self.access_level})"
        )