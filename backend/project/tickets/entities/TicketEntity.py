from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    Ticket,
    TicketField,
)


class TicketEntity(
    BaseEntity
):

    model = Ticket

    entity = "tickets"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "id",

        "type",

        "status",

        "priority",

        "company",

        "executor_group",

        "assigned_to",

        "created_at",
    ]

    search_fields = [
        "id",
    ]

    filter_fields = [

        "type",

        "status",

        "priority",

        "company",

        "executor_group",

        "assigned_to",

        "archived",
    ]

    ordering = [
        "-id",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "tickets.view",

        "view":
            "tickets.view",

        "create":
            "tickets.create",

        "edit":
            "tickets.edit",

        "delete":
            "tickets.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [

            "type",

            "status",

            "priority",

            "company",

            "executor_group",

            "assigned_to",

            "created_by",
        ]

    def get_prefetch_related(self):

        return [

            "dynamic_values",

            "dynamic_values__field",
        ]

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        # =============================================
        # EXISTING TICKET
        # =============================================

        if obj and obj.type_id:

            fieldset = obj.type.fieldset

            if not fieldset:
                return []

            return (

                TicketField.objects

                .filter(
                    fieldset=fieldset,
                )

                .order_by(
                    "order",
                    "id",
                )
            )

        # =============================================
        # CREATE MODE
        # =============================================

        type_id = request.GET.get(
            "type"
        )

        if not type_id:
            return []

        try:

            type_id = int(type_id)

        except (
            TypeError,
            ValueError,
        ):

            return []

        ticket_type = (

            self.model.type.field
            .remote_field.model

            .objects

            .filter(
                pk=type_id
            )

            .select_related(
                "fieldset"
            )

            .first()
        )

        if not ticket_type:
            return []

        if not ticket_type.fieldset:
            return []

        return (

            TicketField.objects

            .filter(
                fieldset=ticket_type.fieldset,
            )

            .order_by(
                "order",
                "id",
            )
        )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {

            "value": obj.pk,

            "label": str(obj),
        }