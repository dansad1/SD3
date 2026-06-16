from django.conf import settings
from django.db import models

from backend.generic.models import TimeStampedModel


class ExecutorGroup(TimeStampedModel):

    name = models.CharField(
        max_length=100,
    )

    companies = models.ManyToManyField(
        "companies.Company",
        related_name="executor_groups",
        blank=True,
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="executor_groups",
        blank=True,
    )

    class Meta:

        ordering = [
            "name",
        ]

    def __str__(self):

        return self.name