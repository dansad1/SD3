# backend/project/notifications/models/EmailSettings.py

from django.db import models

from backend.generic.models import TimeStampedModel


class EmailSettings(TimeStampedModel):

    class Encryption(models.TextChoices):
        NONE = "none", "Без шифрования"
        TLS = "tls", "STARTTLS"
        SSL = "ssl", "SSL/TLS"

    host = models.CharField(
        "SMTP-сервер",
        max_length=255,
    )

    port = models.PositiveIntegerField(
        "Порт",
        default=587,
    )

    host_user = models.CharField(
        "Имя пользователя",
        max_length=255,
        blank=True,
        null=True,
    )

    host_password = models.CharField(
        "Пароль",
        max_length=255,
        blank=True,
        null=True,
    )

    encryption = models.CharField(
        "Шифрование",
        max_length=20,
        choices=Encryption.choices,
        default=Encryption.TLS,
    )

    default_from = models.EmailField(
        "Email отправителя",
    )

    is_active = models.BooleanField(
        "Активно",
        default=True,
    )

    class Meta:
        verbose_name = "Настройки электронной почты"
        verbose_name_plural = "Настройки электронной почты"

    def __str__(self):
        return self.host

    @property
    def use_tls(self):
        return self.encryption == self.Encryption.TLS

    @property
    def use_ssl(self):
        return self.encryption == self.Encryption.SSL
