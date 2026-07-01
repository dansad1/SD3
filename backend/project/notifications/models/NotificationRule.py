from django.db import models

from backend.generic.models import (
    TimeStampedModel,
)
from backend.project.notifications.models.constants import CHANNEL_CHOICES


class NotificationRule(
    TimeStampedModel
):

    event = models.ForeignKey(
        "notifications.NotificationEvent",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="rules",
    )

    ticket_status = models.ForeignKey(
        "tickets.TicketStatus",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notification_rules",
    )

    role = models.ForeignKey(
        "users.UserRole",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="notification_rules",
    )

    logical_role = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    channel = models.CharField(
        max_length=32,
        choices=CHANNEL_CHOICES,
    )

    template = models.ForeignKey(
        "notifications.NotificationTemplate",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="rules",
    )

    enabled = models.BooleanField(
        default=True,
    )

    class Meta:

        ordering = [

            "event",

            "ticket_status",

            "role",

            "logical_role",

            "channel",

        ]

        indexes = [

            models.Index(

                fields=[
                    "event",
                    "role",
                    "channel",
                ],

            ),

            models.Index(

                fields=[
                    "event",
                    "logical_role",
                    "channel",
                ],

            ),

            models.Index(

                fields=[
                    "ticket_status",
                    "role",
                    "channel",
                ],

            ),

            models.Index(

                fields=[
                    "ticket_status",
                    "logical_role",
                    "channel",
                ],

            ),

        ]

        constraints = [

            #
            # Событие + роль
            #

            models.UniqueConstraint(

                fields=[
                    "event",
                    "role",
                    "channel",
                ],

                condition=models.Q(
                    role__isnull=False,
                ),

                name="uniq_notification_event_role_channel",

            ),

            #
            # Событие + логическая роль
            #

            models.UniqueConstraint(

                fields=[
                    "event",
                    "logical_role",
                    "channel",
                ],

                condition=models.Q(
                    logical_role__isnull=False,
                ),

                name="uniq_notification_event_logical_channel",

            ),

            #
            # Статус + роль
            #

            models.UniqueConstraint(

                fields=[
                    "ticket_status",
                    "role",
                    "channel",
                ],

                condition=models.Q(
                    role__isnull=False,
                ),

                name="uniq_notification_status_role_channel",

            ),

            #
            # Статус + логическая роль
            #

            models.UniqueConstraint(

                fields=[
                    "ticket_status",
                    "logical_role",
                    "channel",
                ],

                condition=models.Q(
                    logical_role__isnull=False,
                ),

                name="uniq_notification_status_logical_channel",

            ),

        ]

    def clean(
        self,
    ):

        #
        # Должно быть либо событие,
        # либо статус
        #

        if bool(self.event) == bool(
            self.ticket_status
        ):

            raise ValueError(

                "Необходимо выбрать либо "
                "событие, либо статус."

            )

        #
        # Должна быть либо роль,
        # либо логическая роль
        #

        if bool(self.role) == bool(
            self.logical_role
        ):

            raise ValueError(

                "Необходимо выбрать либо "
                "роль, либо логическую роль."

            )

        #
        # Проверяем,
        # что шаблон поддерживает канал
        #

        if (

            self.template

            and

            self.channel
            not in (
                self.template.channels
                or []
            )

        ):

            raise ValueError(

                "Выбранный шаблон "
                "не поддерживает "
                f"канал '{self.channel}'."

            )

    def __str__(
        self,
    ):

        target = (
            self.event
            or self.ticket_status
        )

        recipient = (
            self.role
            or self.logical_role
        )

        return (

            f"{target}"
            f" → "
            f"{recipient}"
            f" → "
            f"{self.channel}"

        )