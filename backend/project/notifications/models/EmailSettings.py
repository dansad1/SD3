# backend/project/notifications/models/EmailSettings.py

from django.db import models


class EmailSettings(models.Model):

    host = models.CharField(
        max_length=255,
    )

    port = models.PositiveIntegerField(
        default=587,
    )

    host_user = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    host_password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    use_tls = models.BooleanField(
        default=True,
    )

    use_ssl = models.BooleanField(
        default=False,
    )

    default_from = models.EmailField()

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Email settings"
        verbose_name_plural = "Email settings"

    def __str__(self):
        return self.host