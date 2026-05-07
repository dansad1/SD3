from django.db import models

from backend.generic.models import BaseFieldValue


class UserFieldValue(BaseFieldValue):

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="dynamic_values",
    )

    field = models.ForeignKey(
        "users.UserField",
        on_delete=models.CASCADE,
        related_name="values",
    )

    class Meta:

        unique_together = (
            "user",
            "field",
        )

    def __str__(self):

        return (
            f"{self.user} → "
            f"{self.field}"
        )