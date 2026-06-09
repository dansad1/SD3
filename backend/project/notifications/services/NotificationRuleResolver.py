# backend/project/notifications/services/NotificationRuleResolver.py

from backend.project.notifications.models import (
    NotificationRule,
)


class NotificationRuleResolver:

    @classmethod
    def get_rules(
        cls,
        event_code,
    ):
        return (

            NotificationRule.objects

            .filter(

                enabled=True,

                event__code=event_code,
            )

            .select_related(

                "event",

                "role",

                "template",
            )
        )