from django.conf import settings
from django.db import models


class CategoryAssignmentRule(models.Model):

    service = models.ForeignKey(
        "services.Service",
        verbose_name="Сервис",
        on_delete=models.CASCADE,
        related_name="category_rules",
    )

    category = models.ForeignKey(
        "tickets.TicketCategory",
        verbose_name="Категория заявки",
        on_delete=models.CASCADE,
        related_name="assignment_rules",
    )

    executors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Исполнители",
        blank=True,
        related_name="executor_rules",
    )

    executor_groups = models.ManyToManyField(
        "tickets.ExecutorGroup",
        verbose_name="Группы исполнителей",
        blank=True,
        related_name="group_rules",
    )

    watchers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Наблюдатели",
        blank=True,
        related_name="watcher_rules",
    )

    class Meta:

        unique_together = (
            "service",
            "category",
        )

        verbose_name = "Правило назначения категории"
        verbose_name_plural = "Правила назначения категорий"

    def __str__(self):

        return (
            f"{self.service} → "
            f"{self.category}"
        )
