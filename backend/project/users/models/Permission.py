from django.db import models


class Permission(models.Model):

    code = models.CharField(
        max_length=255,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    category = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "category",
            "code",
        ]

    def __str__(self):

        return self.code