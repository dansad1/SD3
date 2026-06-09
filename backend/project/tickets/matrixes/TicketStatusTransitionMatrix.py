# backend/project/tickets/matrixes/TicketStatusTransitionMatrix.py

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)

from backend.project.tickets.models import (
    TicketStatus,
    TicketStatusTransition,
)

from backend.project.users.models import (
    UserRole,
)


class TicketStatusTransitionMatrix(
    BaseMatrix
):

    class Meta:

        code = (
            "ticket-status-transitions"
        )

        capabilities = {

            "view":
                "ticket_transitions.view",

            "edit":
                "ticket_transitions.edit",
        }

    # =====================================
    # SCHEMA
    # =====================================

    def build_schema(
        self,
        request,
    ):
        statuses = list(
            TicketStatus.objects.all()
        )

        roles = list(
            UserRole.objects.all()
        )

        return {

            "rows": [
                {
                    "id": status.id,
                    "label": str(status),
                }
                for status in statuses
            ],

            "columns": [
                {
                    "id": role.id,
                    "label": str(role),
                }
                for role in roles
            ],
        }

    # =====================================
    # DATA
    # =====================================

    def load_data(
        self,
        request,
    ):
        transitions = (

            TicketStatusTransition.objects

            .prefetch_related(
                "allowed_roles",
            )
        )

        result = []

        for transition in transitions:

            for role in (
                transition.allowed_roles.all()
            ):

                result.append({

                    "source":
                        transition.source_id,

                    "target":
                        transition.target_id,

                    "role":
                        role.id,

                    "value":
                        True,
                })

        return {
            "items": result,
        }

    # =====================================
    # SAVE
    # =====================================

    def save_changes(
        self,
        request,
        changes,
    ):
        selected = {

            (
                item["source"],
                item["target"],
                item["role"],
            )

            for item in changes

            if item.get(
                "value"
            )
        }

        current = {

            (
                transition.source_id,
                transition.target_id,
                role.id,
            )

            for transition in (

                TicketStatusTransition.objects

                .prefetch_related(
                    "allowed_roles",
                )
            )

            for role in (
                transition.allowed_roles.all()
            )
        }

        # ADD

        for (
            source_id,
            target_id,
            role_id,
        ) in selected - current:

            transition, _ = (

                TicketStatusTransition.objects

                .get_or_create(

                    source_id=source_id,

                    target_id=target_id,
                )
            )

            transition.allowed_roles.add(
                role_id
            )

        # REMOVE

        for (
            source_id,
            target_id,
            role_id,
        ) in current - selected:

            transition = (

                TicketStatusTransition.objects

                .filter(

                    source_id=source_id,

                    target_id=target_id,

                    allowed_roles=role_id,
                )

                .first()
            )

            if not transition:
                continue

            transition.allowed_roles.remove(
                role_id
            )

            if (
                transition.allowed_roles.count()
                == 0
            ):
                transition.delete()

        return {
            "success": True,
        }