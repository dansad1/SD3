from backend.project.notifications.services.NotificationService import (
    NotificationService,
)


class TicketNotificationService:

    EVENT_CREATED = "ticket.created"
    EVENT_CHANGED = "ticket.changed"

    @classmethod
    def process(
        cls,
        *,
        ticket,
        created=False,
        changes=None,
        user=None,
    ):
        changes = cls.normalize_changes(
            changes
        )

        context = {
            "ticket": ticket,
            "actor": user,
            "user": user,
            "changes": changes,
        }

        # =====================================================
        # CREATED
        # =====================================================

        if created:
            NotificationService.trigger(
                cls.EVENT_CREATED,
                **context,
            )

            return

        # =====================================================
        # CHANGED
        # =====================================================

        if not changes:
            return

        NotificationService.trigger(
            cls.EVENT_CHANGED,
            **context,
        )

    @classmethod
    def normalize_changes(
        cls,
        changes,
    ):
        if not changes:
            return []

        if hasattr(
            changes,
            "to_list",
        ):
            return changes.to_list()

        if isinstance(
            changes,
            list,
        ):
            return changes

        if isinstance(
            changes,
            dict,
        ):
            return changes

        return []