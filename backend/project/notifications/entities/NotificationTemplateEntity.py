from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.notifications.models import (
    NotificationTemplate,
)

from backend.project.notifications.services.NotificationTemplateSchemaService import (
    NotificationTemplateSchemaService,
)


class NotificationTemplateEntity(
    BaseEntity,
):

    model = NotificationTemplate

    entity = "notification-templates"

    list_display = [
        "code",
        "name",
        "channels",
        "is_special",
        "is_active",
    ]

    search_fields = [
        "code",
        "name",
        "subject",
        "body",
    ]

    filter_fields = [
        "channels",
        "is_special",
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
        return []

    def get_prefetch_related(
        self,
    ):
        return [
            "special_users",
        ]

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):
        return (
            NotificationTemplateSchemaService
            .customize(
                request=request,
                schema=schema,
                field=field,
            )
        )

    def get_extra_fields(
        self,
        request,
    ):
        return [
            {
                "name": "variables",
                "label": "Переменные",
                "widget": "InsertVariables",
                "resource": "notification_template.variables",
                "targetField": "body",
            },
        ]