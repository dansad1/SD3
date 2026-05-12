from django.db import models

from backend.generic.models.BaseFieldSet import BaseFieldSet


class UserFieldSet(BaseFieldSet):

    class Meta:

        ordering = [
            "order",
            "id",
        ]

    def __str__(self):
        return self.name