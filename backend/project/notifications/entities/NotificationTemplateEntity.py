# backend/project/notifications/entities/NotificationTemplateEntity.py

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.notifications.models import (
    NotificationTemplate,
)


class NotificationTemplateEntity(
    BaseEntity
):

    model = NotificationTemplate

    entity = "notification-templates"

    list_display = [

        "code",

        "name",

        "channel",

        "event",

        "is_active",
    ]

    search_fields = [

        "code",

        "name",
    ]

    filter_fields = [

        "channel",

        "event",

        "is_active",
    ]

    ordering = [

        "code",
    ]

    capabilities = {

        "list":
            "notifications.templates.view",

        "view":
            "notifications.templates.view",

        "create":
            "notifications.templates.create",

        "edit":
            "notifications.templates.edit",

        "delete":
            "notifications.templates.delete",
    }

    def get_select_related(
        self,
    ):
        return [
            "event",
        ]

    def get_prefetch_related(
        self,
    ):
        return [
            "special_users",
        ]