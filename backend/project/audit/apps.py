from django.apps import AppConfig


class AuditConfig(AppConfig):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "backend.project.audit"

    label = "audit"

    verbose_name = "Аудит"

    def ready(self):

        import backend.project.audit.auth