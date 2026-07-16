class CategoryAssignmentRuleSchemaService:

    READONLY = {
        "id",
    }

    FIELD_SCHEMA = {

        "service": {

            "widget": "entity_select",

            "entity": "service",
        },

        "category": {

            "widget": "entity_select",

            "entity": "ticket_category",
        },

        "executors": {

            "widget": "entity_multiselect",

            "entity": "user",
        },

        "executor_groups": {

            "widget": "entity_multiselect",

            "entity": "executor_group",
        },

        "watchers": {

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

        if name in cls.READONLY:
            schema["readonly"] = True

        config = cls.FIELD_SCHEMA.get(
            name,
        )

        if config:
            schema.update(
                config,
            )

        return schema