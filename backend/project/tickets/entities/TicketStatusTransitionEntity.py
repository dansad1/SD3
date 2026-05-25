from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketStatusTransition,
)


class TicketStatusTransitionEntity(
    BaseEntity
):

    model = TicketStatusTransition

    entity = "ticket-status-transitions"

    list_display = [
        "source",
        "target",
    ]

    filter_fields = [
        "source",
        "target",
    ]

    ordering = [
        "source",
        "target",
    ]

    capabilities = {

        "list":
            "ticket_transitions.view",

        "view":
            "ticket_transitions.view",

        "create":
            "ticket_transitions.create",

        "edit":
            "ticket_transitions.edit",

        "delete":
            "ticket_transitions.delete",
    }

    def get_select_related(self):

        return [
            "source",
            "target",
        ]