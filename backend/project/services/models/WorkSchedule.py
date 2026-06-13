from django.conf import settings
from django.db import models


class WorkSchedule(models.Model):

    name = models.CharField(
        max_length=255,
    )

    owner = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        null=True,
        blank=True,

        on_delete=models.SET_NULL,

        related_name="owned_schedules",
    )

    days = models.ManyToManyField(

        "services.DayOfWeek",

        blank=True,

        related_name="schedules",
    )

    start_time = models.TimeField(
        blank=True,
        null=True,
    )

    end_time = models.TimeField(
        blank=True,
        null=True,
    )

    archived = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:

        ordering = [
            "name",
        ]

    def __str__(self):

        return self.name