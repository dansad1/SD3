from django.db import models

from backend.generic.models.BaseFieldAccess import (
    BaseFieldAccess,
)


class UserFieldAccess(
    BaseFieldAccess,
):

    field = models.ForeignKey(
        "users.UserField",
        verbose_name="Поле пользователя",
        on_delete=models.CASCADE,
        related_name="accesses",
    )

    class Meta(
        BaseFieldAccess.Meta,
    ):

        unique_together = (
            "field",
            "role",
        )

        verbose_name = "Доступ к полю пользователя"
        verbose_name_plural = "Доступы к полям пользователей"
