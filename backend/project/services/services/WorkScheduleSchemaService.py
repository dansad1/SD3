class WorkScheduleSchemaService:

    READONLY_FIELDS = {
        "id",
        "created_at",
        "updated_at",
    }

    FIELD_SCHEMA = {

        "owner": {

            "widget": "entity_select",

            "entity": "user",
        },

        "days": {

            "widget": "entity_multiselect",

            "entity": "day_of_week",
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

        config = cls.FIELD_SCHEMA.get(
            name,
        )

        if config:
            schema.update(
                config,
            )

        return schema