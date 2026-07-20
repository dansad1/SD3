from django.db import models

from backend.generic.models import TimeStampedModel


class Backup(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=255,
    )

    db_path = models.CharField(
        "Путь к базе данных",
        max_length=500,
    )

    media_path = models.CharField(
        "Путь к медиафайлам",
        max_length=500,
        blank=True,
        default="",
    )

    size = models.BigIntegerField(
        "Размер",
        default=0,
    )

    checksum = models.CharField(
        "Контрольная сумма",
        max_length=64,
        blank=True,
        default="",
    )

    class Meta:
        ordering = [
            "-created_at",
        ]
        verbose_name = "Резервная копия"
        verbose_name_plural = "Резервные копии"
