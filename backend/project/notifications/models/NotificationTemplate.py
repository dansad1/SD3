# backend/project/notifications/models/NotificationTemplate.py

from django.db import models


class NotificationTemplate(models.Model):

    CHANNEL_EMAIL = "email"
    CHANNEL_PUSH = "push"
    CHANNEL_SMS = "sms"
    CHANNEL_TELEGRAM = "telegram"

    CHANNEL_CHOICES = [
        (CHANNEL_EMAIL, "Email"),
        (CHANNEL_PUSH, "Push"),
        (CHANNEL_SMS, "SMS"),
        (CHANNEL_TELEGRAM, "Telegram"),
    ]

    code = models.SlugField(
        max_length=100,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    channel = models.CharField(
        max_length=32,
        choices=CHANNEL_CHOICES,
        default=CHANNEL_EMAIL,
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    body = models.TextField()

    event = models.ForeignKey(
        "notifications.NotificationEvent",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="templates",
    )

    is_special = models.BooleanField(
        default=False,
    )

    special_users = models.ManyToManyField(
        "users.User",
        blank=True,
        related_name="special_notification_templates",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "code",
        ]

    def __str__(self):
        return self.code