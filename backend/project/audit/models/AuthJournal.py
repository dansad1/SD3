from django.db import models
from django.conf import settings
from django.utils.timezone import now


class AuthJournal(models.Model):

    ACTIONS = [
        ("login", "Login"),
        ("logout", "Logout"),
        ("failed", "Failed login"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    action = models.CharField(
        max_length=50,
        choices=ACTIONS,
    )

    ip = models.GenericIPAddressField()

    user_agent = models.TextField(
        blank=True,
    )

    meta = models.JSONField(
        default=dict,
        blank=True,
    )

    created = models.DateTimeField(
        default=now,
        db_index=True,
    )

    class Meta:
        ordering = ["-created"]