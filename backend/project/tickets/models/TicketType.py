from django.db import models


class TicketType(models.Model):

    name = models.CharField(
        max_length=100,
    )

    code = models.SlugField(
        max_length=50,
        unique=True,
    )

    fieldset = models.ForeignKey(
        "tickets.TicketFieldSet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="types",
    )

    class Meta:

        ordering = [
            "name",
        ]

    def __str__(self):

        return self.name