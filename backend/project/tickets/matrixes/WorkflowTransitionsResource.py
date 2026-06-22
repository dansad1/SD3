from backend.engine.Resource.BaseResource import BaseResource
from backend.project.tickets.models import (
    TicketStatus,
    TicketStatusTransition,
)
from backend.project.users.models import UserRole


class TicketWorkflowResource(BaseResource):
    code = "ticket.workflow"

    def get(self, request, **params):
        statuses = list(
            TicketStatus.objects.all().order_by("name")
        )
        roles = list(
            UserRole.objects.all().order_by("name")

        )

        transitions = (
            TicketStatusTransition.objects.select_related("source","target").prefetch_related("allowed_roles",))

        by_status = {}

        for tr in transitions:
            by_status.setdefault(
                tr.source_id,{})[tr.target_id] = {"id": tr.pk,

                "roles": [
                    role.name
                    for role in (
                        tr.allowed_roles.all()
                    )
                ],
            }
        result = []

        for source in statuses:
            targets = []
            existing = by_status.get(
                source.pk,
                {},
            )
            for target in statuses:
                if target.pk == source.pk:
                    continue
                transition = existing.get(
                    target.pk,
                    {}
            )
                targets.append(
                    {"id":target.pk,
                        "name":target.name,
                        "roles":transition.get("roles",[],),}

                )

            result.append(

                {

                    "id":source.pk,
                    "name":source.name,
                    "color":source.color,
                    "targets":targets,

                }

            )

        return {

            "roles": [

                {
                    "id":r.pk,
                    "name":r.name,
                }
                for r in roles
            ],
            "statuses":result,
        }