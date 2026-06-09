# backend/project/tickets/services/TicketTimelineService.py

class TicketTimelineService:

    def __init__(
        self,
        ticket,
        user=None,
    ):
        self.ticket = ticket
        self.user = user

    def get_comments(self):
        qs = (
            self.ticket.comments
            .select_related("author")
            .all()
        )

        if not self._can_see_hidden_comments():
            qs = qs.filter(
                hide_from_client=False,
            )

        return [
            {
                "type": "comment",
                "id": comment.id,
                "date": comment.created_at,
                "author": (
                    str(comment.author)
                    if comment.author_id
                    else None
                ),
                "text": comment.text,
                "hide_from_client": comment.hide_from_client,
            }
            for comment in qs
        ]

    def get_logs(self):
        if not hasattr(
            self.ticket,
            "logs",
        ):
            return []

        return [
            {
                "type": "log",
                "id": log.id,
                "date": (
                    log.created_at
                    if hasattr(log, "created_at")
                    else log.timestamp
                ),
                "author": (
                    str(log.author)
                    if getattr(log, "author_id", None)
                    else None
                ),
                "text": getattr(log, "description", ""),
                "event": (
                    str(log.event)
                    if getattr(log, "event_id", None)
                    else None
                ),
            }
            for log in self.ticket.logs.select_related("author").all()
        ]

    def build(self):
        items = (
            self.get_comments()
            + self.get_logs()
        )

        return sorted(
            items,
            key=lambda item: item["date"],
            reverse=True,
        )

    def _can_see_hidden_comments(self):
        user = self.user

        if not user:
            return False

        if user.is_superuser:
            return True

        return user.has_perm(
            "tickets.ticket_comments.view_hidden"
        )