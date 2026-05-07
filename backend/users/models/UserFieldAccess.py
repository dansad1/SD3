from django.db import models


class UserFieldAccess(models.Model):

    ACCESS_NONE = "none"
    ACCESS_VIEW = "view"
    ACCESS_EDIT = "edit"

    ACCESS_CHOICES = [
        (ACCESS_NONE, "Нет доступа"),
        (ACCESS_VIEW, "Просмотр"),
        (ACCESS_EDIT, "Редактирование"),
    ]

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

    access_level = models.CharField(
        max_length=16,
        choices=ACCESS_CHOICES,
        default=ACCESS_NONE,
    )

    class Meta:

        unique_together = (
            "field",
            "role",
        )

    def __str__(self):

        return (
            f"{self.role} → "
            f"{self.field} "
            f"({self.access_level})"
        )