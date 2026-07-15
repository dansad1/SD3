from django.db import models

from backend.project.users.models import UserRole


class BaseFieldAccess(
    models.Model,
):

    ACCESS_VIEW = "view"
    ACCESS_EDIT = "edit"

    ACCESS_CHOICES = [
        (
            ACCESS_VIEW,
            "Просмотр",
        ),
        (
            ACCESS_EDIT,
            "Редактирование",
        ),
    ]

    role = models.ForeignKey(
        UserRole,
        on_delete=models.CASCADE,
    )

    access_level = models.CharField(
        max_length=16,
        choices=ACCESS_CHOICES,
        default=ACCESS_EDIT,
        db_index=True,
    )

    class Meta:

        abstract = True