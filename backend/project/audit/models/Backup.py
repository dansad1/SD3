from django.db import models

from backend.generic.models import TimeStampedModel


class Backup(TimeStampedModel):

    name = models.CharField(
        max_length=255,
    )

    db_path = models.CharField(
        max_length=500,
    )

    media_path = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )

    size = models.BigIntegerField(
        default=0,
    )

    checksum = models.CharField(
        max_length=64,
        blank=True,
        default="",
    )

    class Meta:
        ordering = [
            "-created_at",
        ]