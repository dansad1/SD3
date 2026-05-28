from django.db import models
from django.conf import settings
from django.utils.timezone import now


class EntityJournal(models.Model):

    ACTIONS = [
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
    ]

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    action = models.CharField(
        max_length=50,
        choices=ACTIONS,
    )

    entity = models.CharField(
        max_length=255,
        db_index=True,
    )

    object_id = models.CharField(
        max_length=255,
        db_index=True,
    )

    object_repr = models.CharField(
        max_length=500,
    )

    changes = models.JSONField(
        default=dict,
        blank=True,
    )

    created = models.DateTimeField(
        default=now,
        db_index=True,
    )

    class Meta:
        ordering = ["-created"]