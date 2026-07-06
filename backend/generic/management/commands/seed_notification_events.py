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
                "assigned_by_requester",
                "Назначение заявителем",
                "ticket",
            ),

            (
                "ticket_changed",
                "Изменение заявки",
                "ticket",
            ),

            (
                "comment_created",
                "Новые комментарии в заявке",
                "ticket",
            ),

            (
                "executors_changed",
                "Изменение списка исполнителей",
                "participants",
            ),

            (
                "watchers_changed",
                "Изменение списка наблюдателей",
                "participants",
            ),

            (
                "approvers_changed",
                "Изменение списка согласующих",
                "participants",
            ),

            (
                "executor_group_changed",
                "Изменение группы исполнителей",
                "participants",
            ),

            (
                "execution_expired",
                "Истечение срока исполнения заявки",
                "sla",
            ),

            (
                "reaction_expired",
                "Истечение срока реакции на заявку",
                "sla",
            ),

            (
                "approved",
                "Заявка согласована",
                "approval",
            ),

            (
                "rated",
                "Заявитель оценил заявку",
                "feedback",
            ),

        ]

        synced_codes = []

        for code, name, group in events:

            synced_codes.append(code)

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