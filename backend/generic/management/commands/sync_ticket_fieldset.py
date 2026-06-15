from django.core.management.base import BaseCommand

from backend.project.tickets.models import (
    TicketFieldSet,
    TicketField,
)


class Command(BaseCommand):

    help = (
        "Sync default ticket fieldset "
        "and base ticket fields"
    )

    def handle(
        self,
        *args,
        **kwargs,
    ):

        fieldset, _ = (
            TicketFieldSet.objects
            .get_or_create(
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
                "required": False,

            },

            {
                "name": "due_date",
                "label": "Срок",
                "field_type": "datetime",
                "required": False,

            },

            # =====================================================
            # КЛАССИФИКАЦИЯ
            # =====================================================

            {
                "name": "category",
                "label": "Категория заявки",
                "field_type": "relation",
                "required": False,

            },

            {
                "name": "lifecycle",
                "label": "Жизненный цикл",
                "field_type": "relation",
                "required": False,

            },

            # =====================================================
            # УЧАСТНИКИ
            # =====================================================

            {
                "name": "requester",
                "label": "Заявитель",
                "field_type": "user",
                "required": False,

            },

            {
                "name": "executors",
                "label": "Исполнители",
                "field_type": "user",
                "is_multiple": True,
                "required": False,

            },

            {
                "name": "executor_groups",
                "label": "Группа исполнителей",
                "field_type": "relation",
                "is_multiple": True,
                "required": False,

            },

            {
                "name": "watchers",
                "label": "Наблюдатели",
                "field_type": "user",
                "is_multiple": True,
                "required": False,
            },

            {
                "name": "creator",
                "label": "Создатель",
                "field_type": "user",
                "required": False,
            },

            # =====================================================
            # КОММУНИКАЦИИ
            # =====================================================

            {
                "name": "comment",
                "label": "Комментарий",
                "field_type": "richtext",
                "required": False,

            },

            {
                "name": "hide_comment_from_client",
                "label": "Скрыть комментарий от клиента",
                "field_type": "boolean",
                "required": False,

            },

            # =====================================================
            # ВЛОЖЕНИЯ
            # =====================================================

            {
                "name": "attachments",
                "label": "Вложенные файлы",
                "field_type": "relation",
                "is_multiple": True,
                "required": False,

            },

            # =====================================================
            # СИСТЕМНЫЕ
            # =====================================================

            {
                "name": "system_fields",
                "label": "Системные поля",
                "field_type": "json",
                "required": False,

            },

        ]

        for data in fields:

            field, created = (
                TicketField.objects
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
                "Ticket fieldset synced"
            )
        )