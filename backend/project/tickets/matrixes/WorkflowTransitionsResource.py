# backend/project/tickets/resources/TicketWorkflowResource.py

from backend.engine.Resource.BaseResource import (
    BaseResource,
)
from backend.project.tickets.models import (
    TicketStatus,
    TicketStatusTransition,
)
from backend.project.users.models import (
    UserRole,
)


class TicketWorkflowResource(
    BaseResource,
):
    code = "ticket.workflow"

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        request,
        **params,
    ):
        statuses = list(
            TicketStatus.objects
            .all()
            .order_by(
                "name",
                "pk",
            )
        )

        roles = list(
            UserRole.objects
            .all()
            .order_by(
                "name",
                "pk",
            )
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

        transitions_by_status = {}

        for transition in transitions:
            source_transitions = (
                transitions_by_status.setdefault(
                    transition.source_id,
                    {},
                )
            )

            source_transitions[
                transition.target_id
            ] = {
                "id":
                    transition.pk,

                "roleIds": [
                    role.pk
                    for role
                    in transition.allowed_roles.all()
                ],
            }

        result = []

        for source in statuses:
            targets = []

            existing_transitions = (
                transitions_by_status.get(
                    source.pk,
                    {},
                )
            )

            for target in statuses:
                if target.pk == source.pk:
                    continue

                transition = (
                    existing_transitions.get(
                        target.pk,
                    )
                )

                targets.append({
                    "id":
                        target.pk,

                    "name":
                        target.name,

                    "transitionId": (
                        transition["id"]
                        if transition
                        else None
                    ),

                    "roleIds": (
                        transition["roleIds"]
                        if transition
                        else []
                    ),
                })

            result.append({
                "id":
                    source.pk,

                "name":
                    source.name,

                "color":
                    source.color,

                "targets":
                    targets,
            })

        return {
            "roles": [
                {
                    "id":
                        role.pk,

                    "name":
                        role.name,
                }
                for role in roles
            ],

            "statuses":
                result,
        }