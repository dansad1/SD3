from backend.project.tickets.models import (
    TicketStatus,
)
from backend.project.tickets.services.StatusTransitionService import (
    StatusTransitionService,
)


class TicketSchemaService:

    READONLY_FIELDS = {
        "id",
        "created_at",
        "updated_at",
        "due_date",
    }

    SPECIAL_FIELDS = {
        "lifecycle": {
            "widget": "timeline",
            "label": "Жизненный цикл",
        },
    }

    @classmethod
    def customize(
        cls,
        request,
        schema,
        ticket=None,
    ):
        name = schema.get(
            "name",
        )

        special = cls.SPECIAL_FIELDS.get(
            name,
        )

        if special:
            schema.update(
                special,
            )

        if name in cls.READONLY_FIELDS:
            schema["readonly"] = True

        if name == "status":
            cls.customize_status(
                request=request,
                schema=schema,
                ticket=ticket,
            )

        return schema

    @classmethod
    def customize_status(
        cls,
        request,
        schema,
        ticket=None,
    ):
        if not ticket:
            cls.disable_status_field(
                schema,
            )
            return

        current_status = ticket.get_value(
            "status",
        )

        if not current_status:
            cls.disable_status_field(
                schema,
            )
            return

        role = getattr(
            request.user,
            "role",
            None,
        )

        status_ids = (
            StatusTransitionService
            .get_available_statuses(
                status=current_status,
                role=role,
            )
        )

        statuses = (
            TicketStatus.objects
            .filter(
                pk__in=status_ids,
            )
            .order_by(
                "name",
                "pk",
            )
        )

        schema["options"] = [
            {
                "value": status.pk,
                "label": str(status),
                "color": status.color,
            }
            for status in statuses
        ]

    @classmethod
    def disable_status_field(
        cls,
        schema,
    ):
        schema["options"] = []
        schema["readonly"] = True