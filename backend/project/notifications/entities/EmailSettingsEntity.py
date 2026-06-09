# backend/project/notifications/entities/EmailSettingsEntity.py

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.notifications.models import (
    EmailSettings,
)


class EmailSettingsEntity(
    BaseEntity
):

    model = EmailSettings

    entity = "email-settings"

    list_display = [

        "host",

        "port",

        "default_from",

        "use_tls",

        "use_ssl",

        "is_active",
    ]

    ordering = [
        "id",
    ]

    capabilities = {

        "list":
            "notifications.settings.view",

        "view":
            "notifications.settings.view",

        "create":
            "notifications.settings.edit",

        "edit":
            "notifications.settings.edit",

        "delete":
            "notifications.settings.edit",
    }

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):
        payload = super().validate(
            request,
            payload,
            instance,
        )

        if (
            instance is None
            and self.model.objects.exists()
        ):
            raise ValueError(
                "Email settings already exists"
            )

        return payload