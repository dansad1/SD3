# backend/project/notifications/models/NotificationEvent.py

from django.db import models

from backend.generic.models import TimeStampedModel


class NotificationEvent(TimeStampedModel):

    code = models.SlugField(
        max_length=100,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    group = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "group",
            "name",
        ]

    def __str__(self):
        return self.name