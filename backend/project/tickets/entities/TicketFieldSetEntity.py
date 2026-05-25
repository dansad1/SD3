from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketFieldSet,
)


class TicketFieldSetEntity(
    BaseEntity
):

    model = TicketFieldSet

    entity = "ticket-fieldsets"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "code",
        "name",
        "is_active",
        "is_default",
        "order",
    ]

    search_fields = [
        "code",
        "name",
    ]

    filter_fields = [
        "is_active",
        "is_default",
    ]

    ordering = [
        "order",
        "id",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "ticket_fieldsets.view",

        "view":
            "ticket_fieldsets.view",

        "create":
            "ticket_fieldsets.create",

        "edit":
            "ticket_fieldsets.edit",

        "delete":
            "ticket_fieldsets.delete",
    }