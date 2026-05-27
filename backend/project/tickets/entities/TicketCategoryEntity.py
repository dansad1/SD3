from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketCategory,
)


class TicketCategoryEntity(
    BaseEntity
):

    model = TicketCategory

    entity = "ticket-category"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "name",
        "description",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering = [
        "name",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "ticket_categories.view",

        "view":
            "ticket_categories.view",

        "create":
            "ticket_categories.create",

        "edit":
            "ticket_categories.edit",

        "delete":
            "ticket_categories.delete",
    }