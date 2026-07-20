from django.conf import settings
from django.db import models
from django.utils.timezone import now


class AuthJournal(models.Model):

    ACTIONS = [
        ("login", "Вход"),
        ("logout", "Выход"),
        ("failed", "Неудачная попытка входа"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    action = models.CharField(
        "Действие",
        max_length=50,
        choices=ACTIONS,
    )

    ip = models.GenericIPAddressField(
        "IP-адрес",
    )

    user_agent = models.TextField(
        "User-Agent",
        blank=True,
    )

    meta = models.JSONField(
        "Дополнительные данные",
        default=dict,
        blank=True,
    )

    created = models.DateTimeField(
        "Создано",
        default=now,
        db_index=True,
    )

    class Meta:
        ordering = [
            "-created",
        ]
        verbose_name = "Запись журнала авторизации"
        verbose_name_plural = "Журнал авторизации"
