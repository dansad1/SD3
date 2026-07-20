from django.conf import settings
from django.db import models


class ErrorJournal(models.Model):

    created = models.DateTimeField(
        "Создано",
        auto_now_add=True,
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    exception = models.CharField(
        "Исключение",
        max_length=255,
        db_index=True,
    )

    message = models.TextField(
        "Сообщение",
    )

    traceback = models.TextField(
        "Трассировка",
    )

    path = models.CharField(
        "Путь запроса",
        max_length=1000,
        blank=True,
    )

    method = models.CharField(
        "HTTP-метод",
        max_length=16,
        blank=True,
    )

    ip = models.GenericIPAddressField(
        "IP-адрес",
        null=True,
        blank=True,
    )

    resolved = models.BooleanField(
        "Решено",
        default=False,
        db_index=True,
    )

    meta = models.JSONField(
        "Дополнительные данные",
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = [
            "-created",
        ]
        verbose_name = "Запись журнала ошибок"
        verbose_name_plural = "Журнал ошибок"

    def __str__(self):
        return self.exception
