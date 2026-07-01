from django.db import models

from backend.engine.fields.types.richtext import RichTextFieldType
from backend.generic.models import TimeStampedModel
from backend.project.notifications.models import CHANNEL_CHOICES


class NotificationTemplate(
    TimeStampedModel
):

    code = models.SlugField(
        max_length=100,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    channels = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            "Список каналов, в которых "
            "может использоваться шаблон."
        ),
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    body = models.TextField(
        blank=True,
        default="",
    )
    is_special = models.BooleanField(
        default=False,
    )

    special_users = models.ManyToManyField(
        "users.User",
        blank=True,
        related_name="special_notification_templates",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:

        ordering = [

            "code",

        ]

    def supports_channel(
        self,
        channel,
    ):
        return channel in (
            self.channels
            or []
        )

    @property
    def channel_labels(
        self,
    ):
        mapping = dict(
            CHANNEL_CHOICES,
        )

        return [

            mapping.get(
                channel,
                channel,
            )

            for channel in (
                self.channels
                or []
            )

        ]

    def __str__(
        self,
    ):
        return self.name