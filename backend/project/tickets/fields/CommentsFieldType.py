from django.core.exceptions import ValidationError

from backend.engine.fields.types.base import BaseFieldType
from backend.engine.fields.types.registry import register_field_type
from backend.project.tickets.services.TicketCommentService import (
    TicketCommentService,
)


@register_field_type
class CommentsFieldType(BaseFieldType):
    code = "comments"
    label = "Комментарии"
    widget = "comments"

    sortable = False
    searchable = False
    filterable = False

    features = [
        "hide_from_client",
    ]

    def validate(
            self,
            field,
            value,
    ):
        if value in (
                None,
                "",
                {},
        ):
            return None

        if isinstance(
                value,
                str,
        ):
            value = {
                "text": value,
                "hide_from_client": False,
            }

        if not isinstance(
                value,
                dict,
        ):
            raise ValidationError(
                "Некорректный формат комментария."
            )

        text = str(
            value.get(
                "text",
                "",
            )
        ).strip()

        if not text:
            return None

        return {
            "text": text,
            "hide_from_client": bool(
                value.get(
                    "hide_from_client",
                    False,
                )
            ),
        }

    def normalize(
            self,
            field,
            value,
    ):
        return self.validate(
            field,
            value,
        )

    def serialize(
            self,
            field,
            value,
    ):
        return None

    def deserialize(
            self,
            field,
            value,
    ):
        return None

    def should_save(
            self,
            field,
            value,
    ):
        return False

    def save(
            self,
            instance,
            field,
            value,
            request=None,
    ):
        if not value:
            return None

        if request is None:
            raise ValidationError(
                "Невозможно создать комментарий без request."
            )

        if not request.user.is_authenticated:
            raise ValidationError(
                "Для создания комментария требуется авторизация."
            )

        return TicketCommentService.create(
            ticket=instance,
            author=request.user,
            text=value["text"],
            hide_from_client=value.get(
                "hide_from_client",
                False,
            ),
        )

    def get_schema(
            self,
            field,
            request=None,
            instance=None,
    ):
        schema = super().get_schema(
            field,
            request=request,
            instance=instance,
        )

        schema.update({
            "multiple": False,
            "submit_only": True,
            "clear_after_submit": True,
            "show_hide_from_client": True,
        })

        return schema
