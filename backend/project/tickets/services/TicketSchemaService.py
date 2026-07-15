class TicketSchemaService:

    READONLY_FIELDS = {
        "id",
        "created_at",
        "updated_at",
        "due_date",
    }

    SPECIAL_FIELDS = {

        "lifecycle": {

            "widget": "timeline",

            "label": "Жизненный цикл",

        },

    }

    @classmethod
    def customize(
        cls,
        request,
        schema,
    ):

        name = schema.get(
            "name",
        )

        special = cls.SPECIAL_FIELDS.get(
            name,
        )

        if special:

            schema.update(
                special,
            )

        if name in cls.READONLY_FIELDS:

            schema["readonly"] = True

        return schema