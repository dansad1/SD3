from django.db import models


class Backup(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=255,
    )

    name = models.CharField(
        max_length=255,
    )

    created = models.DateTimeField(
        null=True,
        blank=True,
    )

    db_path = models.CharField(
        max_length=500,
        blank=True,
    )

    media_path = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta:
        managed = False