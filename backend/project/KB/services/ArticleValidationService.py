from django.core.exceptions import (
    ValidationError,
)


class ArticleValidationService:

    PROTECTED_FIELDS = {
        "title",
        "content",
        "tags",
        "section",
    }

    @classmethod
    def validate(
        cls,
        payload,
        instance=None,
    ):
        if instance is None:
            return payload

        if not instance.is_readonly:
            return payload

        cls.validate_readonly_article(
            payload=payload,
            instance=instance,
        )

        return payload

    @classmethod
    def validate_readonly_article(
        cls,
        payload,
        instance,
    ):
        current_values = {
            "title": instance.title,
            "content": instance.content,
            "tags": instance.tags,
            "section": instance.section_id,
        }

        changed_fields = []

        for name in cls.PROTECTED_FIELDS:
            if name not in payload:
                continue

            incoming_value = payload.get(
                name,
            )

            if name == "section":
                incoming_value = cls.normalize_pk(
                    incoming_value,
                )

            if (
                incoming_value
                != current_values[name]
            ):
                changed_fields.append(
                    name,
                )

        if changed_fields:
            raise ValidationError({
                "__all__": [
                    (
                        "Опубликованную или архивную "
                        "статью нельзя редактировать. "
                        "Сначала верните её в черновик."
                    )
                ],
            })

    @staticmethod
    def normalize_pk(
        value,
    ):
        if isinstance(
            value,
            dict,
        ):
            value = value.get(
                "value",
            )

        if value in (
            None,
            "",
        ):
            return None

        try:
            return int(
                value,
            )
        except (
            TypeError,
            ValueError,
        ):
            return value