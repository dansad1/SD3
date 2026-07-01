from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.notifications.models import (
    NotificationTemplate, CHANNEL_CHOICES,
)


class NotificationTemplateEntity(
    BaseEntity
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

        if schema["name"] in {
            "id",
            "created_at",
            "updated_at",
        }:
            schema["readonly"] = True

        if schema["name"] == "channels":
            schema["widget"] = "multiselect"

            schema["options"] = [

                {
                    "value": value,
                    "label": label,
                }

                for value, label in CHANNEL_CHOICES

            ]

        if schema["name"] == "body":
            schema["widget"] = "richtext"

        if schema["name"] == "special_users":
            schema["widget"] = "entity_multiselect"

            schema["entity"] = "user"

        return schema