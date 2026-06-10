from django.core.management.base import BaseCommand

from backend.project.companies.models import (
    CompanyFieldSet,
    CompanyField,
)


class Command(BaseCommand):

    help = (
        "Sync default company fieldset "
        "and base company fields"
    )

    def handle(
        self,
        *args,
        **kwargs,
    ):

        fieldset, _ = (
            CompanyFieldSet.objects
            .get_or_create(
                code="default",
                defaults={
                    "name": "Основной",
                    "is_active": True,
                },
            )
        )

        fields = [

            {
                "name": "name",
                "label": "Название",
                "field_type": "string",
                "required": True,
                "unique": False,
                "is_system": False,
            },

            {
                "name": "full_name",
                "label": "Полное название",
                "field_type": "text",
                "required": False,
                "is_system": False,
            },

            {
                "name": "inn",
                "label": "ИНН",
                "field_type": "string",
                "required": False,
                "unique": True,
                "is_system": False,
            },

            {
                "name": "kpp",
                "label": "КПП",
                "field_type": "string",
                "required": False,
                "is_system": False,
            },

            {
                "name": "ogrn",
                "label": "ОГРН",
                "field_type": "string",
                "required": False,
                "is_system": False,
            },

            {
                "name": "contact_person",
                "label": "Контактное лицо",
                "field_type": "string",
                "required": False,
                "is_system": False,
            },

            {
                "name": "phone",
                "label": "Телефон",
                "field_type": "phone",
                "required": False,
                "is_system": False,
            },

            {
                "name": "email",
                "label": "Email",
                "field_type": "email",
                "required": False,
                "is_system": False,
            },

            {
                "name": "address",
                "label": "Адрес",
                "field_type": "text",
                "required": False,
                "is_system": False,
            },

            {
                "name": "contract_number",
                "label": "Номер договора",
                "field_type": "string",
                "required": False,
                "is_system": False,
            },

            {
                "name": "contract_date",
                "label": "Дата договора",
                "field_type": "date",
                "required": False,
                "is_system": False,
            },

            {
                "name": "comment",
                "label": "Комментарий",
                "field_type": "richtext",
                "required": False,
                "is_system": False,
            },

        ]

        for data in fields:

            field, created = (
                CompanyField.objects
                .update_or_create(
                    fieldset=fieldset,
                    name=data["name"],
                    defaults=data,
                )
            )

            self.stdout.write(
                f"{'🟢' if created else '✔'} "
                f"{field.name}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Company fieldset synced"
            )
        )