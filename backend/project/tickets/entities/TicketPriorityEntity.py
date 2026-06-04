from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketPriority,
)


class TicketPriorityEntity(
    BaseEntity
):

    model = TicketPriority

    entity = "ticket_priorities"

    list_display = [
        "name",
        "level",
        "color",
    ]

    search_fields = [
        "name",
    ]

    ordering = [
        "level",
    ]

    capabilities = {

        "list":
            "ticket_priorities.view",

        "view":
            "ticket_priorities.view",

        "create":
            "ticket_priorities.create",

        "edit":
            "ticket_priorities.edit",

        "delete":
            "ticket_priorities.delete",
    }