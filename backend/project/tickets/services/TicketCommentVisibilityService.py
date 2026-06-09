# backend/project/tickets/services/TicketCommentVisibilityService.py


class TicketCommentVisibilityService:

    @classmethod
    def can_view(
        cls,
        comment,
        user,
    ):
        if not comment.hide_from_client:
            return True

        if not user:
            return False

        if user.is_superuser:
            return True

        return user.has_perm(
            "tickets.view_hidden_comments"
        )

    @classmethod
    def filter_queryset(
        cls,
        queryset,
        user,
    ):
        if not user:
            return queryset.filter(
                hide_from_client=False,
            )

        if user.is_superuser:
            return queryset

        if user.has_perm(
            "tickets.view_hidden_comments"
        ):
            return queryset

        return queryset.filter(
            hide_from_client=False,
        )