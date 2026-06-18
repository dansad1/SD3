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
                "name": "type",
                "label": "Тип заявки",
                "field_type": "relation",
            },

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
                "name": "service",
                "label": "Сервис",
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
                "name": "creator",
                "label": "Создатель",
                "field_type": "user",
            },

            {
                "name": "assigned_to",
                "label": "Ответственный",
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
                "name": "reaction_deadline",
                "label": "Дедлайн реакции",
                "field_type": "datetime",
            },

            {
                "name": "resolve_deadline",
                "label": "Дедлайн решения",
                "field_type": "datetime",
            },

            {
                "name": "closed_at",
                "label": "Закрыта",
                "field_type": "datetime",
            },

            # =====================================================
            # ОЦЕНКА
            # =====================================================

            {
                "name": "rating",
                "label": "Оценка",
                "field_type": "number",
            },

            {
                "name": "feedback",
                "label": "Отзыв",
                "field_type": "text",
            },

            # =====================================================
            # ВЛОЖЕНИЯ
            # =====================================================

            {
                "name": "attachments",
                "label": "Вложения",
                "field_type": "relation",
                "is_multiple": True,
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