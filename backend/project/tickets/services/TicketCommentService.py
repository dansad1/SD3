# backend/project/tickets/services/TicketCommentService.py

from django.core.exceptions import (
    ValidationError,
)

from backend.project.tickets.models import (
    TicketComment,
)


class TicketCommentService:

    @classmethod
    def normalize_text(
        cls,
        text,
    ):
        text = str(
            text or ""
        ).strip()

        return text

    @classmethod
    def validate(
        cls,
        text,
    ):
        text = cls.normalize_text(
            text
        )

        if not text:
            raise ValidationError(
                "Комментарий пуст."
            )

        return text

    @classmethod
    def create(
        cls,
        ticket,
        author,
        text,
        hide=False,
    ):
        text = cls.validate(
            text
        )

        return TicketComment.objects.create(
            ticket=ticket,
            author=author,
            text=text,
            hide_from_client=bool(
                hide
            ),
        )

    @classmethod
    def update(
        cls,
        comment,
        text,
        hide=None,
    ):
        text = cls.validate(
            text
        )

        comment.text = text

        if hide is not None:

            comment.hide_from_client = bool(
                hide
            )

        comment.save()

        return comment

    @classmethod
    def delete(
        cls,
        comment,
    ):
        comment.delete()