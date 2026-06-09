# backend/project/notifications/models/NotificationRule.py

from django.db import models


class NotificationRule(models.Model):

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
        ]

        indexes = [
            models.Index(
                fields=[
                    "event",
                    "role",
                ]
            ),
            models.Index(
                fields=[
                    "ticket_status",
                    "logical_role",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.event or self.ticket_status} → {self.role or self.logical_role}"