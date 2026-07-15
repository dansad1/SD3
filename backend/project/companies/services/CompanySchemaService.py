class CompanySchemaService:

    READONLY_FIELDS = {
        "id",
        "created_at",
        "updated_at",
    }

    @classmethod
    def customize(
        cls,
        request,
        schema,
    ):

        if schema.get(
            "name",
        ) in cls.READONLY_FIELDS:

            schema["readonly"] = True

        return schema