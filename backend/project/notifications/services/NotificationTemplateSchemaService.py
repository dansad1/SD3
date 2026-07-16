from backend.project.notifications.models import (
    CHANNEL_CHOICES,
)


class NotificationTemplateSchemaService:

    READONLY_FIELDS = {
        "id",
        "created_at",
        "updated_at",
    }

    FIELD_SCHEMA = {

        "body": {

            "widget": "richtext",
        },

        "special_users": {

            "widget": "entity_multiselect",

            "entity": "user",
        },

    }

    @classmethod
    def customize(
        cls,
        request,
        schema,
        field=None,
    ):
        name = schema.get(
            "name",
        )

        if name in cls.READONLY_FIELDS:

            schema["readonly"] = True

            return schema

        if name == "channels":

            schema["widget"] = "multiselect"

            schema["options"] = [

                {
                    "value": value,
                    "label": label,
                }

                for value, label
                in CHANNEL_CHOICES

            ]

            return schema

        config = cls.FIELD_SCHEMA.get(
            name,
        )

        if config:

            schema.update(
                config,
            )

        return schema