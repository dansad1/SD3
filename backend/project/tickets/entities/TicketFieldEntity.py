from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    TicketField,
)


class TicketFieldEntity(
    BaseEntity
):

    model = TicketField

    entity = "ticket-fields"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "fieldset",

        "name",

        "label",

        "field_type",

        "required",

        "readonly",

        "hidden",

        "show_in_list",

        "order",
    ]

    search_fields = [
        "name",
        "label",
    ]

    filter_fields = [
        "fieldset",
        "field_type",
    ]

    ordering = [
        "fieldset",
        "order",
        "id",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "ticket_fields.view",

        "view":
            "ticket_fields.view",

        "create":
            "ticket_fields.create",

        "edit":
            "ticket_fields.edit",

        "delete":
            "ticket_fields.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "fieldset",
        ]