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
        "list": "notifications.settings.view",
        "view": "notifications.settings.view",
        "create": "notifications.settings.edit",
        "edit": "notifications.settings.edit",
        "delete": "notifications.settings.edit",
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

        existing = self.model.objects.all()

        if instance is not None:
            existing = existing.exclude(
                pk=instance.pk
            )

        if existing.exists():
            raise ValidationError(
                "SMTP настройки уже существуют"
            )

        use_tls = payload.get(
            "use_tls",
            getattr(instance, "use_tls", False),
        )

        use_ssl = payload.get(
            "use_ssl",
            getattr(instance, "use_ssl", False),
        )

        if use_tls and use_ssl:
            raise ValidationError(
                "Нельзя одновременно использовать "
                "TLS и SSL"
            )

        port = payload.get(
            "port",
            getattr(instance, "port", None),
        )

        if port is None or not 1 <= int(port) <= 65535:
            raise ValidationError({
                "port": "Порт должен быть от 1 до 65535",
            })

        timeout = payload.get(
            "timeout",
            getattr(instance, "timeout", None),
        )

        if timeout is not None and not 1 <= int(timeout) <= 120:
            raise ValidationError({
                "timeout":
                    "Таймаут должен быть от 1 до 120 секунд",
            })

        return payload