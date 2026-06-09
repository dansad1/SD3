# backend/project/tickets/services/TicketCommentService.py

from django.core.exceptions import ValidationError

from backend.project.tickets.models import TicketComment


class TicketCommentService:

    @classmethod
    def normalize_text(cls, text):
        return str(text or "").strip()

    @classmethod
    def validate_text(cls, text):
        text = cls.normalize_text(text)

        if not text:
            raise ValidationError("Комментарий пуст.")

        return text

    @classmethod
    def create(
        cls,
        ticket,
        author,
        text,
        hide_from_client=False,
    ):
        text = cls.validate_text(text)

        return TicketComment.objects.create(
            ticket=ticket,
            author=author,
            text=text,
            hide_from_client=bool(hide_from_client),
        )

    @classmethod
    def update(
        cls,
        comment,
        text,
        hide_from_client=None,
    ):
        text = cls.validate_text(text)

        comment.text = text

        update_fields = [
            "text",
        ]

        if hide_from_client is not None:
            comment.hide_from_client = bool(hide_from_client)
            update_fields.append("hide_from_client")

        comment.save(
            update_fields=update_fields,
        )

        return comment

    @classmethod
    def delete(cls, comment):
        comment.delete()