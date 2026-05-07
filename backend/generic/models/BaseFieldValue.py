import json

from django.db import models


class BaseFieldValue(models.Model):

    value = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True

    @property
    def parsed_value(self):

        if self.value in ("", None):
            return None

        try:
            return json.loads(self.value)
        except Exception:
            return self.value