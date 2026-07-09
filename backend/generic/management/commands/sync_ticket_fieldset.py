from django.core.management.base import BaseCommand
from django.db import transaction

from backend.project.tickets.models import (
    TicketFieldSet,
    TicketField,
)


class Command(BaseCommand):

    help = (
        "Sync default ticket fieldset "
        "and base ticket fields"
    )

    @transaction.atomic
    def handle(
        self,
        *args,
        **kwargs,
    ):

        fieldset, _ = (
            TicketFieldSet.objects
            .update_or_create(
                code="default",
                defaults={
                    "name": "Основной",
                    "is_active": True,
                },
            )
        )

        fields = [

            # =====================================================
            # ОСНОВНОЕ
            # =====================================================

            {
                "name": "name",
                "label": "Название",
                "field_type": "string",
                "required": True,
            },

            {
                "name": "description",
                "label": "Описание",
                "field_type": "richtext",
            },

            {
                "name": "due_date",
                "label": "Срок",
                "field_type": "datetime",
            },

            # =====================================================
            # КЛАССИФИКАЦИЯ
            # =====================================================



            {
                "name": "status",
                "label": "Статус",
                "field_type": "status",
            },

            {
                "name": "priority",
                "label": "Приоритет",
                "field_type": "priority",
            },

            {
                "name": "category",
                "label": "Категория",
                "field_type": "relation",
            },

            {
                "name": "lifecycle",
                "label": "Жизненный цикл",
                "field_type": "relation",
            },

            # =====================================================
            # УЧАСТНИКИ
            # =====================================================

            {
                "name": "requester",
                "label": "Заявитель",
                "field_type": "user",
            },

            {
                "name": "executors",
                "label": "Исполнители",
                "field_type": "user",
                "is_multiple": True,
            },

            {
                "name": "executor_group",
                "label": "Группа исполнителей",
                "field_type": "relation",
            },

            {
                "name": "watchers",
                "label": "Наблюдатели",
                "field_type": "user",
                "is_multiple": True,
            },

            {
                "name": "company",
                "label": "Компания",
                "field_type": "company",
            },

            # =====================================================
            # SLA
            # =====================================================

            {
                "name": "attachments",
                "label": "Вложения",
                "field_type": "relation",
                "is_multiple": True,
            },

        ]

        synced_names = []

        for data in fields:

            synced_names.append(data["name"])

            field, created = (
                TicketField.objects
                .update_or_create(
                    fieldset=fieldset,
                    name=data["name"],
                    defaults=data,
                )
            )

            self.stdout.write(
                f"{'🟢' if created else '✔'} {field.name}"
            )

        # =====================================================
        # DELETE REMOVED FIELDS
        # =====================================================

        deleted, _ = (
            TicketField.objects
            .filter(
                fieldset=fieldset,
            )
            .exclude(
                name__in=synced_names,
            )
            .delete()
        )

        if deleted:
            self.stdout.write(
                self.style.WARNING(
                    f"Удалено полей: {deleted}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Ticket fieldset synchronized."
            )
        )