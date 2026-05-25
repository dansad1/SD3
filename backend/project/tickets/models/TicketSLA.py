from django.db import models


class TicketSLA(models.Model):

    type = models.ForeignKey(
        "tickets.TicketType",
        on_delete=models.CASCADE,
        related_name="slas",
    )

    priority = models.ForeignKey(
        "tickets.TicketPriority",
        on_delete=models.CASCADE,
        related_name="slas",
    )

    hours = models.PositiveIntegerField(
        default=0,
    )

    class Meta:

        unique_together = (
            "type",
            "priority",
        )

        ordering = [
            "type",
            "priority",
        ]

    def __str__(self):

        return (
            f"{self.type} / "
            f"{self.priority} — "
            f"{self.hours} ч."
        )