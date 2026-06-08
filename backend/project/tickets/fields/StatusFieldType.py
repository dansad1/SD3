# backend/engine/fields/types/StatusFieldType.py
from backend.engine.fields.types.relation import RelationFieldType
from backend.project.tickets.models import (
    TicketStatus,
)


class StatusFieldType(
    RelationFieldType
):

    code = "status"

    label = "Статус"

    searchable = False

    sortable = True

    filterable = True

    model = TicketStatus

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):
        """
        Список значений для select.

        Ограничение workflow сюда НЕ кладем.
        Этим занимается TicketTransitionService.
        """

        return TicketStatus.objects.all()

    # =====================================================
    # DISPLAY
    # =====================================================

    def display(
        self,
        value,
    ):
        if not value:
            return "—"

        return str(value)

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
    ):
        schema = super().get_schema(
            field
        )

        schema.update({

            "source":
                "ticket-status",

            "widget":
                "select",
        })

        return schema