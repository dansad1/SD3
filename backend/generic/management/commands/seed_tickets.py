from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction


class Command(BaseCommand):
    help = "Seed базовых справочников заявок"

    @transaction.atomic
    def handle(self, *args, **options):
        TicketPriority = apps.get_model("tickets", "TicketPriority")
        TicketStatus = apps.get_model("tickets", "TicketStatus")
        TicketType = apps.get_model("tickets", "TicketType")

        priorities = [
            ("Критический", 1, "#d32f2f"),
            ("Высокий", 2, "#f57c00"),
            ("Средний", 3, "#fbc02d"),
            ("Низкий", 4, "#388e3c"),
            ("Плановый", 5, "#1976d2"),
        ]

        for name, level, color in priorities:
            TicketPriority.objects.update_or_create(
                level=level,
                defaults={
                    "name": name,
                    "color": color,
                },
            )

        statuses = [
            {
                "code": "new",
                "name": "Новая",
                "color": "#1976d2",
            },
            {
                "code": "in_progress",
                "name": "В работе",
                "color": "#f57c00",
            },
            {
                "code": "waiting_user",
                "name": "Ожидает пользователя",
                "color": "#7b1fa2",
                "blocks_time": True,
            },
            {
                "code": "waiting_vendor",
                "name": "Ожидает подрядчика",
                "color": "#455a64",
                "blocks_time": True,
            },
            {
                "code": "resolved",
                "name": "Решена",
                "color": "#388e3c",
                "comment_required": True,
                "blocks_editing": True,
            },
            {
                "code": "closed",
                "name": "Закрыта",
                "color": "#616161",
                "blocks_editing": True,
            },
            {
                "code": "cancelled",
                "name": "Отменена",
                "color": "#9e9e9e",
                "comment_required": True,
                "blocks_time": True,
                "blocks_editing": True,
            },
        ]

        for item in statuses:
            TicketStatus.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "color": item.get("color", "#999999"),
                    "comment_required": item.get("comment_required", False),
                    "blocks_time": item.get("blocks_time", False),
                    "blocks_editing": item.get("blocks_editing", False),
                },
            )

        types = [
            ("incident", "Инцидент"),
            ("service_request", "Запрос на обслуживание"),
            ("access_request", "Запрос доступа"),
            ("consultation", "Консультация"),
            ("change_request", "Запрос на изменение"),
            ("hardware", "Оборудование"),
            ("software", "Программное обеспечение"),
        ]

        for code, name in types:
            TicketType.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "fieldset": None,
                },
            )

        self.stdout.write(
            self.style.SUCCESS("Справочники заявок засеяны, можно запускаться.")
        )