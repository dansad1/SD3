from django.core.exceptions import ValidationError

from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.project.notifications.models import EmailSettings


class EmailSettingsEntity(BaseEntity):

    model = EmailSettings
    entity = "email-settings"

    include_fields = [
        "host",
        "port",
        "host_user",
        "host_password",
        "encryption",
        "default_from",
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

    # =====================================================
    # SINGLETON
    # =====================================================

    def resolve_pk(
        self,
        request,
        mode,
        pk,
    ):
        if pk:
            return pk

        return (
            self.model.objects
            .order_by("id")
            .values_list(
                "pk",
                flat=True,
            )
            .first()
        )

    # =====================================================
    # VALIDATION
    # =====================================================

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

        port = payload.get(
            "port",
            getattr(
                instance,
                "port",
                None,
            ),
        )

        try:
            port = int(port)

        except (
            TypeError,
            ValueError,
        ):
            raise ValidationError({
                "port": "Некорректный порт",
            })

        if not 1 <= port <= 65535:
            raise ValidationError({
                "port":
                    "Порт должен быть от 1 до 65535",
            })

        encryption = payload.get(
            "encryption",
            getattr(
                instance,
                "encryption",
                EmailSettings.Encryption.TLS,
            ),
        )

        allowed_encryption = {
            EmailSettings.Encryption.NONE,
            EmailSettings.Encryption.TLS,
            EmailSettings.Encryption.SSL,
        }

        if encryption not in allowed_encryption:
            raise ValidationError({
                "encryption":
                    "Некорректный режим шифрования",
            })

        return payload