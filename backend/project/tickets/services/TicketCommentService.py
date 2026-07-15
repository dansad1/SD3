from django.core.exceptions import (
    PermissionDenied,
    ValidationError,
)
from django.utils import timezone

from backend.project.tickets.models import (
    TicketComment,
)


class TicketCommentService:

    @classmethod
    def normalize_text(
        cls,
        text,
    ):
        return str(
            text or "",
        ).strip()

    @classmethod
    def validate_text(
        cls,
        text,
    ):
        text = cls.normalize_text(
            text,
        )

        if not text:
            raise ValidationError(
                "Комментарий пуст.",
            )

        return text

    @classmethod
    def can_edit(
        cls,
        user,
        comment,
    ):
        if user.is_superuser:
            return True

        return (
            comment.author_id
            == user.pk
        )

    @classmethod
    def create(
        cls,
        ticket,
        author,
        text,
        hide_from_client=False,
    ):
        return TicketComment.objects.create(
            ticket=ticket,
            author=author,
            text=cls.validate_text(
                text,
            ),
            hide_from_client=hide_from_client,
        )

    @classmethod
    def update(
        cls,
        user,
        comment,
        text,
        hide_from_client,
    ):
        if not cls.can_edit(
            user,
            comment,
        ):
            raise PermissionDenied

        comment.text = cls.validate_text(
            text,
        )

        comment.hide_from_client = (
            hide_from_client
        )

        comment.edited_at = (
            timezone.now()
        )

        comment.edited_by = user

        comment.save()

        return comment

    @classmethod
    def delete(
        cls,
        user,
        comment,
    ):
        if not cls.can_edit(
            user,
            comment,
        ):
            raise PermissionDenied

        comment.delete()