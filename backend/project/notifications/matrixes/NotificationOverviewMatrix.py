# backend/project/notifications/matrixes/NotificationOverviewMatrix.py

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)

from backend.project.notifications.models import (
    NotificationRule,
    NotificationEvent,
)

from backend.project.users.models import (
    UserRole,
)


LOGICAL_ROLES = [
    "requester",
    "assignee",
]


class NotificationOverviewMatrix(
    BaseMatrix
):

    class Meta:

        code = "notification-overview"

        capabilities = {
            "view":
                "notifications.rules.view",
        }

    def build_schema(
        self,
        request,
    ):
        roles = list(
            UserRole.objects.all()
        )

        return {

            "roles": [

                {
                    "id":
                        f"role:{role.id}",

                    "label":
                        role.name,
                }

                for role in roles
            ],

            "logical_roles": [

                {
                    "id":
                        f"logical:{key}",

                    "label":
                        key,
                }

                for key in LOGICAL_ROLES
            ],
        }

    def load_data(
        self,
        request,
    ):
        rules = (

            NotificationRule.objects

            .select_related(
                "event",
                "role",
            )
        )

        events = list(
            NotificationEvent.objects
            .filter(
                is_active=True,
            )
            .order_by(
                "group",
                "name",
            )
        )

        role_matrix = {}

        logical_matrix = {}

        for rule in rules:

            if not rule.event_id:
                continue

            if rule.role_id:

                role_matrix[
                    (
                        rule.event_id,
                        rule.role_id,
                    )
                ] = True

            if rule.logical_role:

                logical_matrix[
                    (
                        rule.event_id,
                        rule.logical_role,
                    )
                ] = True

        return {

            "events": [

                {
                    "id":
                        event.id,

                    "name":
                        event.name,

                    "group":
                        event.group,
                }

                for event in events
            ],

            "role_matrix":
                role_matrix,

            "logical_matrix":
                logical_matrix,
        }

    def save_changes(
        self,
        request,
        changes,
    ):
        return {
            "success": True,
        }