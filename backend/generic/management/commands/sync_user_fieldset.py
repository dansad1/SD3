from django.core.management.base import BaseCommand

from backend.project.users.models import (
    UserFieldSet,
    UserField,
)


class Command(BaseCommand):

    help = "Sync default user fieldset and base user fields"

    def handle(self, *args, **kwargs):

        fieldset, _ = UserFieldSet.objects.get_or_create(
            code="default",
            defaults={
                "name": "Основной",
                "is_active": True,
            },
        )

        fields = [

            {
                "name": "login",
                "label": "Логин",
                "field_type": "string",
                "required": True,
                "unique": True,
                "is_system": True,
            },

            {
                "name": "full_name",
                "label": "ФИО",
                "field_type": "string",
                "required": False,
                "is_system": False,
            },

            {
                "name": "email",
                "label": "Email",
                "field_type": "email",
                "required": False,
                "unique": True,
                "is_system": False,
            },

            {
                "name": "company",
                "label": "Компания",
                "field_type": "relation",
                "required": False,
                "is_system": False,
                "is_multiple": False,
                "options": {
                    "entity": "company",
                },
            },

            {
                "name": "phone",
                "label": "Телефон",
                "field_type": "phone",
                "required": False,
                "is_system": False,
            },

            {
                "name": "telegram",
                "label": "Telegram",
                "field_type": "string",
                "required": False,
                "is_system": False,
            },

            {
                "name": "department",
                "label": "Отдел",
                "field_type": "string",
                "required": False,
                "is_system": False,
            },

        ]
        for data in fields:
            field, created = UserField.objects.update_or_create(
                fieldset=fieldset,
                name=data["name"],
                defaults=data,
            )

            self.stdout.write(
                f"{'🟢' if created else '✔'} {field.name}"
            )

        self.stdout.write(
            self.style.SUCCESS("User fieldset synced")
        )