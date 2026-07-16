# backend/project/notifications/entities/NotificationRuleEntity.py

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.notifications.models import (
    NotificationRule,
)


class NotificationRuleEntity(
    BaseEntity
):
    model = NotificationRule
    entity = "notification-rules"

    list_display = [
        "event",
        "ticket_status",
        "role",
        "logical_role",
        "template",
        "enabled",
    ]

    filter_fields = [

        "event",
        "ticket_status",
        "role",
        "logical_role",
        "enabled",
    ]

    ordering = [
        "event",
        "ticket_status",
    ]

    capabilities = {

        "list":
            "notifications.rules.view",

        "view":
            "notifications.rules.view",

        "create":
            "notifications.rules.create",

        "edit":
            "notifications.rules.edit",

        "delete":
            "notifications.rules.delete",
    }

    def get_select_related(
        self,
    ):
        return [
            "event",
            "ticket_status",
            "role",
            "template",
        ]