from django.db import models

from backend.generic.models import BaseFieldValue


class UserFieldValue(BaseFieldValue):

    user = models.ForeignKey(
        "users.User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "users.UserField",
        verbose_name="Поле пользователя",
        on_delete=models.CASCADE,
        related_name="values",
    )

    class Meta:

        unique_together = (
            "user",
            "field",
        )

        verbose_name = "Значение поля пользователя"
        verbose_name_plural = "Значения полей пользователей"

    def __str__(self):

        return (
            f"{self.user} → "
            f"{self.field}"
        )
