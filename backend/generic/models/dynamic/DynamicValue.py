from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from SD3.backend.generic.models.dynamic.DynamicField import DynamicField


class DynamicValue(models.Model):
    field = models.ForeignKey(
        DynamicField,
        on_delete=models.CASCADE,
        related_name="values"
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    value = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("field", "content_type", "object_id")

        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["field"]),
        ]

    def __str__(self):
        return f"{self.field} = {self.value}"