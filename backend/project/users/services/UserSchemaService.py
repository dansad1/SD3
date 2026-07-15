class UserSchemaService:

    READONLY_FIELDS = {
        "created_at",
        "updated_at",
        "last_login",
    }

    HIDDEN_FOR_NON_SUPERUSER = {
        "is_superuser",
        "is_staff",
    }

    SPECIAL_FIELDS = {

        "password": {

            "widget": "password",

            "writeonly": True,

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

        if (
            not request.user.is_superuser
            and name in cls.HIDDEN_FOR_NON_SUPERUSER
        ):

            schema["hidden"] = True

        return schema