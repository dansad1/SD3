from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketStatus,
)


class TicketStatusEntity(
    BaseEntity
):

    model = TicketStatus

    entity = "ticket-statuses"

    list_display = [

        "name",

        "code",

        "color",

        "comment_required",

        "blocks_time",

        "blocks_editing",
    ]

    search_fields = [
        "name",
        "code",
    ]

    ordering = [
        "name",
    ]

    capabilities = {

        "list":
            "ticket_statuses.view",

        "view":
            "ticket_statuses.view",

        "create":
            "ticket_statuses.create",

        "edit":
            "ticket_statuses.edit",

        "delete":
            "ticket_statuses.delete",
    }