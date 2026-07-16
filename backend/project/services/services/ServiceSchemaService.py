class ServiceSchemaService:

    READONLY_FIELDS = {
        "id",
        "created_at",
        "updated_at",
    }

    FIELD_SCHEMA = {
        "users": {
            "widget": "entity_multiselect",
            "entity": "user",
        },
        "companies": {
            "widget": "entity_multiselect",
            "entity": "company",
        },
        "roles": {
            "widget": "entity_multiselect",
            "entity": "user_role",
        },
        "ticket_categories": {
            "widget": "entity_multiselect",
            "entity": "ticket_category",
        },
        "ticket_types": {
            "widget": "entity_multiselect",
            "entity": "ticket_type",
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

        if name == "parent":
            schema["filter"] = {
                "archived": False,
            }

        field_schema = cls.FIELD_SCHEMA.get(
            name,
        )

        if field_schema:
            schema.update(
                field_schema,
            )

        return schema