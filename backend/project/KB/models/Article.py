from ckeditor.fields import RichTextField
from django.db import models
from backend.generic.models import TimeStampedModel


class Article(TimeStampedModel):

    title = models.CharField(
        max_length=500,
    )

    section = models.ForeignKey(
        "KB.ArticleSection",
        related_name="articles",
        on_delete=models.PROTECT,
    )

    content = RichTextField()

    is_published = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title