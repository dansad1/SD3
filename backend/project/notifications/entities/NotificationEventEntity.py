# backend/project/notifications/entities/NotificationEventEntity.py

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.notifications.models import (
    NotificationEvent,
)


class NotificationEventEntity(
    BaseEntity
):

    model = NotificationEvent

    entity = "notification-events"

    list_display = [

        "code",

        "name",

        "group",

        "is_active",
    ]

    search_fields = [

        "code",

        "name",
    ]

    filter_fields = [

        "group",

        "is_active",
    ]

    ordering = [

        "group",

        "name",
    ]

    capabilities = {

        "list":
            "notifications.events.view",

        "view":
            "notifications.events.view",

        "create":
            "notifications.events.create",

        "edit":
            "notifications.events.edit",

        "delete":
            "notifications.events.delete",
    }