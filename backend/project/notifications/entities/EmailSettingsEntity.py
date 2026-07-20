from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.project.notifications.models import EmailSettings
from backend.project.notifications.services.EmailSettingsSingletonService import (
    EmailSettingsSingletonService,
)
from backend.project.notifications.services.EmailSettingsValidationService import (
    EmailSettingsValidationService,
)


class EmailSettingsEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = EmailSettings

    entity = "email-settings"

    # =====================================================
    # UI
    # =====================================================

    ordering = [
        "id",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

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
        return EmailSettingsSingletonService.resolve_pk(
            model=self.model,
            pk=pk,
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
            request=request,
            payload=payload,
            instance=instance,
        )

        return EmailSettingsValidationService.validate(
            payload=payload,
            instance=instance,
        )