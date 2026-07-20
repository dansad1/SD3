# backend/project/notifications/models/NotificationEvent.py

from django.db import models

from backend.generic.models import TimeStampedModel


class NotificationEvent(TimeStampedModel):

    code = models.SlugField(
        "Код",
        max_length=100,
        unique=True,
    )

    name = models.CharField(
        "Название",
        max_length=255,
    )

    group = models.CharField(
        "Группа",
        max_length=100,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        "Активно",
        default=True,
    )

    class Meta:
        ordering = [
            "group",
            "name",
        ]
        verbose_name = "Событие уведомления"
        verbose_name_plural = "События уведомлений"

    def __str__(self):
        return self.name
