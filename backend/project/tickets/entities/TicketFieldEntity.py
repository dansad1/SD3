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

    entity = "ticket-field"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "name",

        "label",

        "field_type",

        "required",

        "unique",


    ]

    search_fields = [
        "name",
        "label",
    ]

    filter_fields = [
        "field_type",
    ]

    exclude_fields = [
        "fieldset",
        "created_at",
        "updated_at",
        "choices",
        "options"
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

    # =====================================================
    # FORM
    # =====================================================

    def get_fields(
        self,
        request,
        obj=None,
    ):

        fields = super().get_fields(
            request,
            obj,
        )

        return [

            field

            for field in fields

            if field.name != "fieldset"
        ]
