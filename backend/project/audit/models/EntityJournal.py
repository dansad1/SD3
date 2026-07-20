from django.conf import settings
from django.db import models
from django.utils.timezone import now


class EntityJournal(models.Model):

    ACTIONS = [
        ("create", "Создание"),
        ("update", "Изменение"),
        ("delete", "Удаление"),
    ]

    actor = models.ForeignKey(
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

    entity = models.CharField(
        "Сущность",
        max_length=255,
        db_index=True,
    )

    object_id = models.CharField(
        "Идентификатор объекта",
        max_length=255,
        db_index=True,
    )

    object_repr = models.CharField(
        "Представление объекта",
        max_length=500,
    )

    changes = models.JSONField(
        "Изменения",
        default=dict,
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
        verbose_name = "Запись журнала сущности"
        verbose_name_plural = "Журнал сущностей"
