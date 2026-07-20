from django.conf import settings
from django.db import models


class UserListSettings(models.Model):

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

        verbose_name = "Настройки списка пользователя"
        verbose_name_plural = "Настройки списков пользователей"
