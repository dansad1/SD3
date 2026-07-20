from django.conf import settings
from django.db import models


class CompanyListSettings(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )

    entity = models.CharField(
        "Сущность",
        max_length=255,
    )

    visible_fields = models.JSONField(
        "Видимые поля",
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
            "Настройки списка компаний"
        )

        verbose_name_plural = (
            "Настройки списков компаний"
        )

    def __str__(self):

        return (
            f"{self.user} → "
            f"{self.entity}"
        )
