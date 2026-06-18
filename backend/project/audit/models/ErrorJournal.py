from django.conf import settings
from django.db import models


class ErrorJournal(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    exception = models.CharField(
        max_length=255,
        db_index=True,
    )

    message = models.TextField()

    traceback = models.TextField()

    path = models.CharField(
        max_length=1000,
        blank=True,
    )

    method = models.CharField(
        max_length=16,
        blank=True,
    )

    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    resolved = models.BooleanField(
        default=False,
        db_index=True,
    )

    meta = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.exception