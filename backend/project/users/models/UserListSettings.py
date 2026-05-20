from django.db import models
from django.conf import settings


class UserListSettings(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    entity = models.CharField(
        max_length=255,
    )

    visible_fields = models.JSONField(
        default=list,
        blank=True,
    )

    class Meta:
        unique_together = (
            "user",
            "entity",
        )