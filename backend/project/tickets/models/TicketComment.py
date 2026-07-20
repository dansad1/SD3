from django.conf import settings
from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)


class TicketComment(
    TimeStampedModel,
):

    ticket = models.ForeignKey(
        "tickets.Ticket",
        verbose_name="Заявка",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_comments",
    )

    text = models.TextField(
        "Текст комментария",
    )

    hide_from_client = models.BooleanField(
        "Скрыть от клиента",
        default=False,
    )

    edited_at = models.DateTimeField(
        "Дата редактирования",
        null=True,
        blank=True,
    )

    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Отредактировал",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:

        verbose_name = (
            "Комментарий заявки"
        )

        verbose_name_plural = (
            "Комментарии заявок"
        )

        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return (
            f"Комментарий #{self.pk}"
        )
