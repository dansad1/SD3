from backend.engine.Resource.BaseResource import BaseResource
from backend.project.tickets.models import TicketStatus, TicketStatusTransition


class TicketWorkflowResource(BaseResource):
    code = "ticket.workflow"

    def get(self, request, **params):

        statuses = list(
            TicketStatus.objects
            .all()
            .order_by("name")
        )

        transitions = (
            TicketStatusTransition.objects
            .select_related(
                "source",
                "target",
            )
            .prefetch_related(
                "allowed_roles",
            )
        )

        existing = {}

        for t in transitions:

            existing[
                (
                    t.source_id,
                    t.target_id,
                )
            ] = {

                "id": t.pk,

                "roles": [

                    r.name

                    for r in t.allowed_roles.all()

                ],

            }

        result = []

        for source in statuses:

            items = []

            for target in statuses:

                if source.pk == target.pk:
                    continue

                tr = existing.get(
                    (
                        source.pk,
                        target.pk,
                    )
                )

                items.append(

                    {

                        "target_id":
                            target.pk,

                        "target":
                            target.name,

                        "exists":
                            tr is not None,

                        "transition_id":

                            tr["id"]

                            if tr

                            else None,

                        "roles":

                            tr["roles"]

                            if tr

                            else [],

                    }

                )

            result.append(

                {

                    "id":
                        source.pk,

                    "name":
                        source.name,

                    "color":
                        source.color,

                    "items":
                        items,

                }

            )

        return {

            "statuses":

                result

        }