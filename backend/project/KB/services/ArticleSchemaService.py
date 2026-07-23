class ArticleSchemaService:

    SPECIAL_FIELDS = {
        "title": {
            "label": "Заголовок",
        },
        "section": {
            "label": "Раздел",
        },
        "content": {
            "type": "richtext",
            "widget": "richtext",
            "label": "Содержание",
        },
        "tags": {
            "label": "Теги",
        },
        "status": {
            "label": "Статус",
            "required": True,
            "clearable": False,
            "allow_empty": False,
            "nullable": False,
        },
    }

    EDITABLE_WHEN_READONLY = {
        "status",
    }

    @classmethod
    def customize(
        cls,
        request,
        schema,
        article=None,
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

        if (
            article is not None
            and article.is_readonly
            and name not in cls.EDITABLE_WHEN_READONLY
        ):
            schema["readonly"] = True

        return schema