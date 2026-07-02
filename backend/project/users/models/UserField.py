from django.db import models

from backend.generic.models.BaseField import (
    BaseField,
)

class UserField(BaseField):

    fieldset = models.ForeignKey(
        "users.UserFieldSet",
        on_delete=models.CASCADE,
        related_name="fields",
        blank=True,
        null=True,
    )

    @property
    def value_model(self):
        from backend.project.users.models import (
            UserFieldValue,
        )

        return UserFieldValue

    class Meta:
        unique_together = (
            "fieldset",
            "name",
        )

    def __str__(self):
        return (
            f"{self.fieldset}: "
            f"{self.label}"
        )