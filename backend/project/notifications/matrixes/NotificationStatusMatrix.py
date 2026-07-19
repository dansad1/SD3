from django.core.exceptions import ValidationError
from django.db import transaction

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)
from backend.project.notifications.models import (
    CHANNEL_CHOICES,
    NotificationEvent,
    NotificationRule,
    NotificationTemplate,
)
from backend.project.tickets.models import (
    TicketStatus,
)


class NotificationStatusMatrix(BaseMatrix):

    class Meta:
        code = "notification-status"

        capabilities = {
            "view": "notifications.rules.view",
            "edit": "notifications.rules.edit",
        }

    # =====================================================
    # SCHEMA
    # =====================================================

    def build_schema(
        self,
        request,
    ):
        templates = list(
            NotificationTemplate.objects
            .filter(
                is_active=True,
            )
            .order_by(
                "name",
            )
        )

        statuses = list(
            TicketStatus.objects
            .order_by(
                "name",
            )
        )

        channel_options = {
            code: []
            for code, _ in CHANNEL_CHOICES
        }

        for template in templates:
            template_channels = (
                template.channels
                or []
            )

            for channel in template_channels:
                if channel not in channel_options:
                    continue

                channel_options[channel].append({
                    "value": template.pk,
                    "label": template.name,
                })

        return {
            "layoutRows": [
                {
                    "id": str(status.pk),
                    "label": status.name,
                }
                for status in statuses
            ],
            "layoutColumns": [
                {
                    "id": code,
                    "label": label,
                }
                for code, label in CHANNEL_CHOICES
            ],
            "defaultCell": {
                "widget": "select",
            },
            "columnSchema": {
                code: {
                    "widget": "select",
                    "options": channel_options.get(
                        code,
                        [],
                    ),
                }
                for code, _ in CHANNEL_CHOICES
            },
            "rowSchema": {},
            "cells": {},
        }

    # =====================================================
    # DATA
    # =====================================================

    def load_data(
        self,
        request,
    ):
        event_code = self.get_param(
            request,
            "event",
        )

        recipient = self.get_param(
            request,
            "recipient",
        )

        if not event_code or not recipient:
            return {
                "items": [],
            }

        event = self.get_event(
            event_code,
        )

        recipient_type, recipient_value = (
            self.parse_recipient(
                recipient,
            )
        )

        queryset = (
            NotificationRule.objects
            .filter(
                enabled=True,
                event=event,
                ticket_status__isnull=False,
            )
            .select_related(
                "event",
                "ticket_status",
                "template",
                "role",
            )
        )

        if recipient_type == "role":
            queryset = queryset.filter(
                role_id=recipient_value,
                logical_role="",
            )

        elif recipient_type == "logical":
            queryset = queryset.filter(
                logical_role=recipient_value,
                role_id__isnull=True,
            )

        return {
            "items": [
                {
                    "row": str(
                        rule.ticket_status_id
                    ),
                    "column": rule.channel,
                    "value": rule.template_id,
                }
                for rule in queryset
            ],
        }

    # =====================================================
    # SAVE
    # =====================================================

    @transaction.atomic
    def save_changes(
        self,
        request,
        changes,
    ):
        event_code = self.get_param(
            request,
            "event",
        )

        recipient = self.get_param(
            request,
            "recipient",
        )

        if not event_code:
            raise ValidationError(
                "Событие не выбрано"
            )

        if not recipient:
            raise ValidationError(
                "Получатель не выбран"
            )

        event = self.get_event(
            event_code,
        )

        recipient_type, recipient_value = (
            self.parse_recipient(
                recipient,
            )
        )

        allowed_channels = {
            code
            for code, _ in CHANNEL_CHOICES
        }

        for change in changes or []:
            if not isinstance(
                change,
                dict,
            ):
                continue

            row = (
                change.get("row")
                or change.get("y")
            )

            column = (
                change.get("column")
                or change.get("x")
            )

            value = change.get(
                "value",
            )

            if isinstance(
                value,
                dict,
            ):
                value = (
                    value.get("value")
                    or value.get("id")
                )

            status_id = self.parse_status_id(
                row,
            )

            if not column:
                raise ValidationError(
                    "Не указана колонка матрицы"
                )

            if column not in allowed_channels:
                raise ValidationError(
                    f"Неизвестный канал: {column}"
                )

            lookup = {
                "event": event,
                "ticket_status_id": status_id,
                "channel": column,
            }

            if recipient_type == "role":
                lookup.update({
                    "role_id": recipient_value,
                    "logical_role": "",
                })

            elif recipient_type == "logical":
                lookup.update({
                    "role_id": None,
                    "logical_role": recipient_value,
                })

            if value in (
                None,
                "",
                0,
                "0",
            ):
                NotificationRule.objects.filter(
                    **lookup,
                ).delete()

                continue

            template = self.get_template(
                template_id=value,
                channel=column,
            )

            NotificationRule.objects.update_or_create(
                **lookup,
                defaults={
                    "template": template,
                    "enabled": True,
                },
            )

        return {
            "success": True,
        }

    # =====================================================
    # HELPERS
    # =====================================================

    def get_event(
        self,
        event_code,
    ):
        event_code = str(
            event_code
        ).strip()

        if not event_code:
            raise ValidationError(
                "Событие не выбрано"
            )

        event = (
            NotificationEvent.objects
            .filter(
                code=event_code,
            )
            .first()
        )

        if event is None:
            raise ValidationError(
                f"Событие {event_code} не найдено"
            )

        return event

    def get_template(
        self,
        *,
        template_id,
        channel,
    ):
        try:
            template_id = int(
                template_id
            )

        except (
            TypeError,
            ValueError,
        ):
            raise ValidationError(
                "Некорректный шаблон"
            )

        template = (
            NotificationTemplate.objects
            .filter(
                pk=template_id,
                is_active=True,
            )
            .first()
        )

        if template is None:
            raise ValidationError(
                "Шаблон не найден или отключён"
            )

        template_channels = (
            template.channels
            or []
        )

        if channel not in template_channels:
            raise ValidationError(
                "Шаблон не поддерживает выбранный канал"
            )

        return template

    def parse_status_id(
        self,
        value,
    ):
        if value in (
            None,
            "",
        ):
            raise ValidationError(
                "Не указана строка матрицы"
            )

        try:
            status_id = int(
                value
            )

        except (
            TypeError,
            ValueError,
        ):
            raise ValidationError(
                "Некорректный статус заявки"
            )

        status_exists = (
            TicketStatus.objects
            .filter(
                pk=status_id,
            )
            .exists()
        )

        if not status_exists:
            raise ValidationError(
                "Статус заявки не найден"
            )

        return status_id

    def parse_recipient(
        self,
        recipient,
    ):
        recipient = str(
            recipient
        ).strip()

        if recipient.startswith(
            "role:",
        ):
            raw_value = recipient.split(
                ":",
                1,
            )[1]

            try:
                role_id = int(
                    raw_value
                )

            except (
                TypeError,
                ValueError,
            ):
                raise ValidationError(
                    "Некорректная роль"
                )

            return (
                "role",
                role_id,
            )

        if recipient.startswith(
            "logical:",
        ):
            logical_role = recipient.split(
                ":",
                1,
            )[1].strip()

            if not logical_role:
                raise ValidationError(
                    "Некорректный логический получатель"
                )

            return (
                "logical",
                logical_role,
            )

        raise ValidationError(
            "Неизвестный тип получателя"
        )