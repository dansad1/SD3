from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)


class StoredFile(TimeStampedModel):

    file = models.FileField(
        upload_to="uploads/%Y/%m/",
    )

    original_name = models.CharField(
        max_length=255,
    )

    mime_type = models.CharField(
        max_length=255,
        blank=True,
    )

    size = models.BigIntegerField(
        default=0,
    )

    uploaded_by = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="uploaded_files",
    )

    class Meta:

        verbose_name = "Файл"

        verbose_name_plural = "Файлы"

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return (
            self.original_name
            or f"File #{self.pk}"
        )