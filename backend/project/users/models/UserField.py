from django.db import models

from backend.generic.models.BaseField import BaseField


class UserField(BaseField):

    fieldset = models.ForeignKey(
        "users.UserFieldSet",
        on_delete=models.CASCADE,
        related_name="fields",
    )

    class Meta:

        ordering = [
            "order",
            "id",
        ]

        unique_together = (
            "fieldset",
            "name",
        )

    def __str__(self):
        return f"{self.fieldset}: {self.label}"