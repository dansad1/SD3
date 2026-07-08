from backend.engine.fields.providers.BaseRelationProvider import (
    BaseRelationProvider,
)

from backend.engine.fields.providers.registry import (
    register_relation_provider,
)
from backend.project.tickets.models import TicketStatus


@register_relation_provider
class StatusProvider(
    BaseRelationProvider,
):

    code = "status"

    def get_initial(
        self,
        field,
        request=None,
        instance=None,
    ):

        if field.name != "status":
            return None

        return (
            TicketStatus.objects
            .filter(
                code="low",
            )
            .first()
        )