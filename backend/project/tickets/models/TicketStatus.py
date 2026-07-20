from django.db import models

from backend.generic.models import TimeStampedModel


class TicketStatus(TimeStampedModel):

    name = models.CharField(
        "Название",
        max_length=100,
    )

    code = models.SlugField(
        "Код",
        max_length=50,
        unique=True,
    )

    color = models.CharField(
        "Цвет",
        max_length=7,
        default="#999999",
    )

    comment_required = models.BooleanField(
        "Комментарий обязателен",
        default=False,
    )

    blocks_time = models.BooleanField(
        "Приостанавливает отсчёт времени",
        default=False,
    )

    blocks_editing = models.BooleanField(
        "Блокирует редактирование",
        default=False,
    )

    class Meta:

        ordering = [
            "name",
        ]

        verbose_name = (
            "Статус заявки"
        )

        verbose_name_plural = (
            "Статусы заявок"
        )

    def __str__(self):

        return self.name
