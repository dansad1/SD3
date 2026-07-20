from django.db import models

from backend.generic.models import TimeStampedModel
from backend.project.users.models.Permission import (
    Permission,
)


class UserRole(TimeStampedModel):

    code = models.SlugField(
        "Код",
        max_length=100,
        unique=True,
    )

    name = models.CharField(
        "Название",
        max_length=255,
    )

    description = models.TextField(
        "Описание",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        "Активна",
        default=True,
    )

    is_executor = models.BooleanField(
        "Роль исполнителя",
        default=False,
    )

    permissions = models.ManyToManyField(
        Permission,
        verbose_name="Разрешения",
        blank=True,
        related_name="roles",
    )

    class Meta:

        ordering = [
            "name",
        ]

        verbose_name = "Роль пользователя"
        verbose_name_plural = "Роли пользователей"

    def __str__(self):

        return self.name
