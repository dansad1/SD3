from django.db import models

from backend.generic.models import TimeStampedModel


class ArticleSection(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=255,
    )

    parent = models.ForeignKey(
        "self",
        verbose_name="Родительский раздел",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    sort_order = models.IntegerField(
        "Порядок сортировки",
        default=0,
    )

    class Meta:

        ordering = [
            "sort_order",
            "name",
        ]

        verbose_name = "Раздел базы знаний"
        verbose_name_plural = "Разделы базы знаний"

    def __str__(self):

        return self.name
