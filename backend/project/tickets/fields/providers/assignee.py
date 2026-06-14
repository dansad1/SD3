from backend.engine.fields.providers.registry import (
    relation_provider_registry,
)

from backend.project.tickets.services.TicketAssignmentPolicy import (
    TicketAssignmentPolicy,
)


def assignee_provider(
    request=None,
    **kwargs,
):

    if not request:
        return []

    return (
        TicketAssignmentPolicy
        .get_allowed_assignees(
            request.user
        )
    )


relation_provider_registry.register(
    "assignee",
    assignee_provider,
)