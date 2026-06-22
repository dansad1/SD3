from collections import defaultdict

from backend.engine.Resource.BaseResource import BaseResource
from backend.project.notifications.models import (
    NotificationEvent,
    NotificationRule,
)
from backend.project.users.models import UserRole


LOGICAL_ROLE_LABELS = {
    "requester": "Заявитель",
    "executor": "Исполнитель",
    "dispatcher": "Диспетчер группы исполнителей",
    "member": "Член группы исполнителей",
    "watcher": "Наблюдатель",
    "approver": "Согласующий",
}


class NotificationOverviewResource(BaseResource):

    code = "notification.overview"

    def get(
        self,
        request,
        **kwargs,
    ):

        events = list(
            NotificationEvent.objects.all()
        )

        rules = list(

            NotificationRule.objects.filter(

                enabled=True,

            ).select_related(

                "event",

                "ticket_status",

                "role",

            )

        )

        by_role = defaultdict(list)

        by_logical_role = defaultdict(list)

        for rule in rules:

            if rule.role_id:

                by_role[
                    rule.role_id
                ].append(rule)

            if rule.logical_role:

                by_logical_role[
                    rule.logical_role
                ].append(rule)

        roles = []

        for role in UserRole.objects.all():

            role_rules = by_role.get(

                role.pk,

                [],
            )

            roles.append({

                "id":
                    role.pk,

                "label":
                    str(role),

                "events":

                    sorted({

                        r.event.code

                        for r in role_rules

                        if r.event_id

                    }),

                "statuses":

                    sorted({

                        r.ticket_status.name

                        for r in role_rules

                        if r.ticket_status_id

                    }),

            })

        logical_roles = []

        for logical_role, label in (
            LOGICAL_ROLE_LABELS.items()
        ):

            role_rules = by_logical_role.get(

                logical_role,

                [],
            )

            logical_roles.append({

                "code":
                    logical_role,

                "label":
                    label,

                "events":

                    sorted({

                        r.event.code

                        for r in role_rules

                        if r.event_id

                    }),

                "statuses":

                    sorted({

                        r.ticket_status.name

                        for r in role_rules

                        if r.ticket_status_id

                    }),

            })

        return {

            "events": [

                {

                    "code":
                        event.code,

                    "label":
                        event.name,

                }

                for event in events

            ],

            "roles":
                roles,

            "logical_roles":
                logical_roles,

        }