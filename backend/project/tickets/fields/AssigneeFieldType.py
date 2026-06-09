# backend/engine/fields/types/AssigneeFieldType.py

from backend.engine.fields.types.UserFieldType import (
    UserFieldType,
)

from backend.project.tickets.services.TicketAssignmentPolicy import (
    TicketAssignmentPolicy,
)


class AssigneeFieldType(
    UserFieldType
):

    code = "assignee"

    label = "Исполнитель"

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):
        if not request:
            return []

        return (
            TicketAssignmentPolicy
            .get_allowed_assignees(
                request.user
            )
        )

    def display(
        self,
        value,
    ):
        if not value:
            return "—"

        if hasattr(
            value,
            "get_full_name",
        ):
            full_name = (
                value.get_full_name()
            )

            if full_name:
                return full_name

        return (
            getattr(
                value,
                "username",
                None,
            )
            or str(value)
        )

    def get_schema(
        self,
        field,
    ):
        schema = super().get_schema(
            field
        )

        schema.update({
            "widget": "select",
            "source": "assignee",
        })

        return schema