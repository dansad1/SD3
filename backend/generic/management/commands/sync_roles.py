from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Синхронизация системных ролей"

    @transaction.atomic
    def handle(self, *args, **options):
        Permission = apps.get_model(
            "users",
            "Permission",
        )

        UserRole = apps.get_model(
            "users",
            "UserRole",
        )

        roles = [
            {
                "code": "admin",
                "name": "Администратор",
                "description": "Полный доступ к системе.",
                "permissions": "*",
            },
            {
                "code": "helpdesk_manager",
                "name": "Руководитель Service Desk",
                "description": "Управление пользователями, компаниями и заявками.",
                "permissions": [
                    "users.view",
                    "users.create",
                    "users.edit",
                    "users.delete",

                    "companies.view",
                    "companies.create",
                    "companies.edit",
                    "companies.delete",

                    "tickets.view",
                    "tickets.create",
                    "tickets.edit",
                    "tickets.delete",
                ],
            },
            {
                "code": "dispatcher",
                "name": "Диспетчер",
                "description": "Принимает и распределяет заявки.",
                "permissions": [
                    "tickets.view",
                    "tickets.create",
                    "tickets.edit",

                    "companies.view",

                    "users.view",
                ],
            },
            {
                "code": "senior_executor",
                "name": "Старший исполнитель",
                "description": "Работает с заявками и помогает исполнителям.",
                "is_executor": True,
                "permissions": [
                    "tickets.view",
                    "tickets.edit",

                    "companies.view",

                    "users.view",
                ],
            },
            {
                "code": "executor",
                "name": "Исполнитель",
                "description": "Выполняет назначенные заявки.",
                "is_executor": True,
                "permissions": [
                    "tickets.view",
                    "tickets.edit",
                ],
            },
            {
                "code": "company_manager",
                "name": "Представитель компании",
                "description": "Создает заявки своей компании.",
                "permissions": [
                    "tickets.view",
                    "tickets.create",

                    "companies.view",
                ],
            },
            {
                "code": "observer",
                "name": "Наблюдатель",
                "description": "Только просмотр.",
                "permissions": [
                    "tickets.view",
                    "companies.view",
                    "users.view",
                ],
            },
            {
                "code": "auditor",
                "name": "Аудитор",
                "description": "Просмотр всех данных.",
                "permissions": [
                    "tickets.view",
                    "companies.view",
                    "users.view",
                ],
            },
        ]

        permissions = {
            permission.code: permission
            for permission in Permission.objects.all()
        }

        role_codes = []

        for item in roles:
            role_codes.append(
                item["code"]
            )

            role, _ = (
                UserRole.objects.update_or_create(
                    code=item["code"],
                    defaults={
                        "name": item["name"],
                        "description": item["description"],
                        "is_active": True,
                        "is_executor": item.get(
                            "is_executor",
                            False,
                        ),
                    },
                )
            )

            if item["permissions"] == "*":
                role.permissions.set(
                    Permission.objects.all()
                )
            else:
                role.permissions.set(
                    [
                        permissions[code]
                        for code in item["permissions"]
                        if code in permissions
                    ]
                )

        UserRole.objects.exclude(
            code__in=role_codes,
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Системные роли синхронизированы."
            )
        )