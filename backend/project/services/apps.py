from django.apps import AppConfig


class ServicesConfig(AppConfig):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "backend.project.services"

    label = "services"

    verbose_name = "Сервисы"