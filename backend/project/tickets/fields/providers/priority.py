from backend.engine.fields.providers.BaseRelationProvider import (
    BaseRelationProvider,
)

from backend.engine.fields.providers.registry import (
    register_relation_provider,
)
from backend.project.tickets.models import TicketPriority


@register_relation_provider
class PriorityProvider(
    BaseRelationProvider,
):

    code = "priority"

    def get_initial(
        self,
        field,
        request=None,
        instance=None,
    ):

        if field.name != "priority":
            return None

        return (
            TicketPriority.objects
            .filter(
                level=5,
            )
            .first()
        )