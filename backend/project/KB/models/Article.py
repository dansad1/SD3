from ckeditor.fields import RichTextField
from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=500)

    section = models.ForeignKey(
        "KB.ArticleSection",
        related_name="articles",
        on_delete=models.PROTECT,
    )

    content = RichTextField()

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title