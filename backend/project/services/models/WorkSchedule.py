from django.conf import settings
from django.db import models


class WorkSchedule(models.Model):

    name = models.CharField(
        "Название",
        max_length=255,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="owned_schedules",
    )

    days = models.ManyToManyField(
        "services.DayOfWeek",
        verbose_name="Дни недели",
        blank=True,
        related_name="schedules",
    )

    start_time = models.TimeField(
        "Время начала",
        blank=True,
        null=True,
    )

    end_time = models.TimeField(
        "Время окончания",
        blank=True,
        null=True,
    )

    archived = models.BooleanField(
        "Архивирован",
        default=False,
    )

    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        "Обновлён",
        auto_now=True,
        editable=False,
    )

    class Meta:

        ordering = [
            "name",
        ]

        verbose_name = "График работы"
        verbose_name_plural = "Графики работы"

    def __str__(self):

        return self.name
