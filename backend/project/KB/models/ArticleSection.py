from django.db import models

from backend.generic.models import TimeStampedModel


class ArticleSection(TimeStampedModel):

    name = models.CharField(max_length=255)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name