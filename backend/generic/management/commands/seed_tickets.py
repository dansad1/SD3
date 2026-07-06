from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Полная синхронизация системных справочников заявок"

    @transaction.atomic
    def handle(self, *args, **options):
        TicketPriority = apps.get_model(
            "tickets",
            "TicketPriority",
        )
        TicketStatus = apps.get_model(
            "tickets",
            "TicketStatus",
        )
        TicketType = apps.get_model(
            "tickets",
            "TicketType",
        )
        TicketFieldSet = apps.get_model(
            "tickets",
            "TicketFieldSet",
        )

        # =====================================================
        # DEFAULT FIELDSET
        # =====================================================

        default_fieldset, _ = (
            TicketFieldSet.objects.update_or_create(
                code="default",
                defaults={
                    "name": "Основной",
                    "is_active": True,
                },
            )
        )

        # =====================================================
        # PRIORITIES
        # =====================================================

        priorities = [
            ("Критический", 1, "#d32f2f"),
            ("Высокий", 2, "#f57c00"),
            ("Средний", 3, "#fbc02d"),
            ("Низкий", 4, "#388e3c"),
            ("Плановый", 5, "#1976d2"),
        ]

        priority_levels = []

        for name, level, color in priorities:
            priority_levels.append(level)

            TicketPriority.objects.update_or_create(
                level=level,
                defaults={
                    "name": name,
                    "color": color,
                },
            )

        TicketPriority.objects.exclude(
            level__in=priority_levels,
        ).delete()

        # =====================================================
        # STATUSES
        # =====================================================

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

        status_codes = []

        for item in statuses:
            status_codes.append(item["code"])

            TicketStatus.objects.update_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "color": item.get(
                        "color",
                        "#999999",
                    ),
                    "comment_required": item.get(
                        "comment_required",
                        False,
                    ),
                    "blocks_time": item.get(
                        "blocks_time",
                        False,
                    ),
                    "blocks_editing": item.get(
                        "blocks_editing",
                        False,
                    ),
                },
            )

        TicketStatus.objects.exclude(
            code__in=status_codes,
        ).delete()

        # =====================================================
        # TYPES
        # =====================================================

        types = [
            ("incident", "Инцидент"),
            (
                "service_request",
                "Запрос на обслуживание",
            ),
            (
                "access_request",
                "Запрос доступа",
            ),
            (
                "consultation",
                "Консультация",
            ),
            (
                "change_request",
                "Запрос на изменение",
            ),
            (
                "hardware",
                "Оборудование",
            ),
            (
                "software",
                "Программное обеспечение",
            ),
        ]

        type_codes = []

        for code, name in types:
            type_codes.append(code)

            TicketType.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "fieldset": default_fieldset,
                },
            )

        TicketType.objects.exclude(
            code__in=type_codes,
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Системные справочники полностью синхронизированы."
            )
        )