# backend/project/tickets/services/TicketNotificationService.py


class TicketNotificationService:
    """
    Заглушка-адаптер.

    Сюда потом подключаем вашу старую trigger_event /
    notification template систему.
    """

    @staticmethod
    def ticket_created(
        ticket,
        user,
        context=None,
    ):
        return None

    @staticmethod
    def ticket_updated(
        ticket,
        user,
        changes=None,
        context=None,
    ):
        return None

    @staticmethod
    def comment_added(
        ticket,
        comment,
        user,
        context=None,
    ):
        return None

    @staticmethod
    def attachment_added(
        ticket,
        attachment,
        user,
        context=None,
    ):
        return None

    @staticmethod
    def attachment_deleted(
        ticket,
        attachment_id,
        user,
        context=None,
    ):
        return None