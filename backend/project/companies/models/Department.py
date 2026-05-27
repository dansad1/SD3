# =========================================================
# MODELS
# backend/project/companies/models/Department.py
# =========================================================

from django.conf import settings
from django.db import models


class Department(models.Model):

    # =====================================================
    # RELATIONS
    # =====================================================

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name="Компания",
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="Родительский отдел",
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="departments",
        verbose_name="Пользователи",
    )

    # =====================================================
    # STATIC FIELDS
    # =====================================================

    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    archived = models.BooleanField(
        default=False,
        verbose_name="Архивирован",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлён",
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        verbose_name = "Отдел"

        verbose_name_plural = "Отделы"

        ordering = [
            "name",
        ]

    # =====================================================
    # STR
    # =====================================================

    def __str__(self):

        return self.get_full_path()

    # =====================================================
    # TREE
    # =====================================================

    def get_full_path(self):

        parts = [self.name]

        parent = self.parent

        while parent:

            parts.append(
                parent.name
            )

            parent = parent.parent

        return " / ".join(
            reversed(parts)
        )

    # =====================================================
    # HELPERS
    # =====================================================

    @property
    def has_children(self):

        return self.children.exists()