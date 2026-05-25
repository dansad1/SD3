from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketSLA,
)


class TicketSLAEntity(
    BaseEntity
):

    model = TicketSLA

    entity = "ticket-slas"

    list_display = [
        "type",
        "priority",
        "hours",
    ]

    filter_fields = [
        "type",
        "priority",
    ]

    ordering = [
        "type",
        "priority",
    ]

    capabilities = {

        "list":
            "ticket_slas.view",

        "view":
            "ticket_slas.view",

        "create":
            "ticket_slas.create",

        "edit":
            "ticket_slas.edit",

        "delete":
            "ticket_slas.delete",
    }

    def get_select_related(self):

        return [
            "type",
            "priority",
        ]