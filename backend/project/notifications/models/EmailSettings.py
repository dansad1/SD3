# backend/project/notifications/models/EmailSettings.py

from django.db import models

from backend.generic.models import TimeStampedModel


class EmailSettings(TimeStampedModel):

    class Encryption(models.TextChoices):
        NONE = "none", "Без шифрования"
        TLS = "tls", "STARTTLS"
        SSL = "ssl", "SSL/TLS"

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

    encryption = models.CharField(
        max_length=20,
        choices=Encryption.choices,
        default=Encryption.TLS,
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

    @property
    def use_tls(self):
        return self.encryption == self.Encryption.TLS

    @property
    def use_ssl(self):
        return self.encryption == self.Encryption.SSL