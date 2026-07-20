from ckeditor.fields import RichTextField
from django.db import models

from backend.generic.models import TimeStampedModel


class Article(TimeStampedModel):

    title = models.CharField(
        "Заголовок",
        max_length=500,
    )

    section = models.ForeignKey(
        "KB.ArticleSection",
        verbose_name="Раздел",
        related_name="articles",
        on_delete=models.PROTECT,
    )

    content = RichTextField(
        "Содержание",
    )

    is_published = models.BooleanField(
        "Опубликована",
        default=True,
    )

    class Meta:

        ordering = [
            "title",
        ]

        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):

        return self.title
