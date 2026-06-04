from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketType,
)


class TicketTypeEntity(
    BaseEntity
):

    model = TicketType

    entity = "ticket-type"

    list_display = [
        "name",
        "code",
        "fieldset",
    ]

    search_fields = [
        "name",
        "code",
    ]

    filter_fields = [
        "fieldset",
    ]

    ordering = [
        "name",
    ]

    capabilities = {

        "list":
            "ticket_types.view",

        "view":
            "ticket_types.view",

        "create":
            "ticket_types.create",

        "edit":
            "ticket_types.edit",

        "delete":
            "ticket_types.delete",
    }

    def get_select_related(self):

        return [
            "fieldset",
        ]