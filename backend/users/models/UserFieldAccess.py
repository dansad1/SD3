from django.db import models


class UserFieldAccess(models.Model):

    field = models.ForeignKey(
        "users.UserField",
        on_delete=models.CASCADE,
        related_name="accesses",
    )

    role = models.ForeignKey(
        "users.UserRole",
        on_delete=models.CASCADE,
        related_name="field_accesses",
    )

    can_view = models.BooleanField(
        default=True,
    )

    can_edit = models.BooleanField(
        default=True,
    )

    class Meta:

        unique_together = (
            "field",
            "role",
        )

    def __str__(self):

        return (
            f"{self.role} → "
            f"{self.field}"
        )