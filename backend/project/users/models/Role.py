from django.db import models


from django.db import models

from backend.generic.models import TimeStampedModel
from backend.project.users.models.Permission import (
    Permission
)


class UserRole(TimeStampedModel):

    code = models.SlugField(
        max_length=100,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    priority = models.IntegerField(
        default=0,
    )

    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="roles",
    )



    class Meta:

        ordering = [
            "priority",
            "name",
        ]

    def __str__(self):

        return self.name