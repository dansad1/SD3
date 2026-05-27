from django.conf import settings
from django.db import models


class CategoryAssignmentRule(models.Model):

    service = models.ForeignKey(

        "services.Service",

        on_delete=models.CASCADE,

        related_name="category_rules",
    )

    category = models.ForeignKey(

        "tickets.TicketCategory",

        on_delete=models.CASCADE,

        related_name="assignment_rules",
    )

    executors = models.ManyToManyField(

        settings.AUTH_USER_MODEL,

        blank=True,

        related_name="executor_rules",
    )

    executor_groups = models.ManyToManyField(

        "tickets.ExecutorGroup",

        blank=True,

        related_name="group_rules",
    )

    watchers = models.ManyToManyField(

        settings.AUTH_USER_MODEL,

        blank=True,

        related_name="watcher_rules",
    )

    class Meta:

        unique_together = (
            "service",
            "category",
        )

    def __str__(self):

        return (
            f"{self.service} → "
            f"{self.category}"
        )