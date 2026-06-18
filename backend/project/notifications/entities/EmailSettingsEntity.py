from django.core.exceptions import ValidationError

from backend.engine.entity.Base.BaseEntity import BaseEntity

from backend.project.notifications.models import EmailSettings


class EmailSettingsEntity(BaseEntity):

    model = EmailSettings

    entity = "email-settings"

    include_fields = [

        "host",
        "port",

        "username",
        "password",

        "default_from",

        "timeout",

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
            raise ValidationError(
                "SMTP настройки уже существуют"
            )

        if (
                payload.get("use_tls")
                and payload.get("use_ssl")
        ):
            raise ValidationError(
                "Нельзя одновременно использовать TLS и SSL"
            )

        return payload