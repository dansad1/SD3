from django.conf import settings
from django.db import models

from backend.generic.models import TimeStampedModel


class ExecutorGroup(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=100,
    )

    companies = models.ManyToManyField(
        "companies.Company",
        verbose_name="Компании",
        related_name="executor_groups",
        blank=True,
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователи",
        related_name="executor_groups",
        blank=True,
    )

    class Meta:

        ordering = [
            "name",
        ]

        verbose_name = "Группа исполнителей"
        verbose_name_plural = "Группы исполнителей"

    def __str__(self):

        return self.name
