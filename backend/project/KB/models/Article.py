from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)


class Article(TimeStampedModel):

    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (
            STATUS_DRAFT,
            "Черновик",
        ),
        (
            STATUS_PUBLISHED,
            "Опубликована",
        ),
        (
            STATUS_ARCHIVED,
            "В архиве",
        ),
    ]

    title = models.CharField(
        "Заголовок",
        max_length=255,
    )

    section = models.ForeignKey(
        "KB.ArticleSection",
        verbose_name="Раздел",
        related_name="articles",
        on_delete=models.PROTECT,
    )

    content = models.TextField(
        "Содержание",
        blank=True,
        default="",
    )

    tags = models.JSONField(
        "Теги",
        blank=True,
        default=list,
    )

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        db_index=True,
    )

    class Meta:
        ordering = [
            "-updated_at",
        ]

        verbose_name = (
            "Статья базы знаний"
        )
        verbose_name_plural = (
            "Статьи базы знаний"
        )

    def __str__(self):
        return self.title

    @property
    def is_readonly(self):
        return self.status in {
            self.STATUS_PUBLISHED,
            self.STATUS_ARCHIVED,
        }