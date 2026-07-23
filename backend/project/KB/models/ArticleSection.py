from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)
from backend.project.users.models import (
    UserRole,
)


class ArticleSection(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=255,
    )

    sort_order = models.PositiveIntegerField(
        "Порядок",
        default=0,
        db_index=True,
    )

    user_roles = models.ManyToManyField(
        UserRole,
        verbose_name="Роли пользователей",
        related_name="article_sections",
        blank=True,
    )

    class Meta:
        ordering = [
            "sort_order",
            "name",
        ]

        verbose_name = (
            "Раздел базы знаний"
        )
        verbose_name_plural = (
            "Разделы базы знаний"
        )

    def __str__(self):
        return self.name