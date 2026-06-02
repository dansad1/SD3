from django.db import models

from django.contrib.contenttypes.fields import (
    GenericForeignKey,
)

from django.contrib.contenttypes.models import (
    ContentType,
)


class DynamicValue(models.Model):

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    object_id = models.PositiveBigIntegerField()

    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    field_name = models.CharField(
        max_length=100,
        db_index=True,
    )

    value = models.TextField(
        null=True,
        blank=True,
    )

    class Meta:

        unique_together = (
            "content_type",
            "object_id",
            "field_name",
        )