from django.db import models
from django.conf import settings


class CompanyListSettings(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,
    )

    entity = models.CharField(
        max_length=255,
    )

    visible_fields = models.JSONField(

        default=list,

        blank=True,
    )

    class Meta:

        unique_together = (
            "user",
            "entity",
        )

        ordering = [
            "entity",
            "id",
        ]

        verbose_name = (
            "Company list settings"
        )

        verbose_name_plural = (
            "Company list settings"
        )

    def __str__(self):

        return (
            f"{self.user} → "
            f"{self.entity}"
        )