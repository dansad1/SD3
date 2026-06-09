# backend/project/tickets/services/TicketAssignmentValidator.py

from django.core.exceptions import (
    ValidationError,
)

from backend.project.tickets.services.TicketAssignmentPolicy import (
    TicketAssignmentPolicy,
)


class TicketAssignmentValidator:

    @classmethod
    def validate(
        cls,
        actor,
        assignee,
    ):
        if not assignee:
            return

        if not (
            TicketAssignmentPolicy
            .can_assign(
                actor,
                assignee,
            )
        ):
            raise ValidationError(
                "Недопустимый исполнитель."
            )