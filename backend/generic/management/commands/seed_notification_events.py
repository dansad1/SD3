from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):

    help = "Seed notification events"

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):

        NotificationEvent = apps.get_model(
            "notifications",
            "NotificationEvent",
        )

        events = [

            (
                "ticket.created",
                "Создание заявки",
                "ticket",
            ),

            (
                "ticket.changed",
                "Изменение заявки",
                "ticket",
            ),

            (
                "ticket.closed",
                "Закрытие заявки",
                "ticket",
            ),

            (
                "ticket.comment_added",
                "Добавлен комментарий",
                "comments",
            ),

            (
                "ticket.approved",
                "Заявка согласована",
                "approval",
            ),

            (
                "ticket.reaction_expired",
                "Истечение срока реакции",
                "sla",
            ),

            (
                "ticket.execution_expired",
                "Истечение срока исполнения",
                "sla",
            ),

            (
                "ticket.rated",
                "Получена оценка",
                "feedback",
            ),

        ]

        synced_codes = []

        for code, name, group in events:

            synced_codes.append(
                code,
            )

            event, created = (
                NotificationEvent.objects
                .update_or_create(
                    code=code,
                    defaults={
                        "name": name,
                        "group": group,
                        "is_active": True,
                    },
                )
            )

            self.stdout.write(
                f"{'🟢' if created else '✔'} {event.code}"
            )

        deleted, _ = (
            NotificationEvent.objects
            .exclude(
                code__in=synced_codes,
            )
            .delete()
        )

        if deleted:

            self.stdout.write(
                self.style.WARNING(
                    f"Удалено событий: {deleted}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Notification events synchronized."
            )
        )