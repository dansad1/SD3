from django.core.exceptions import (
    ValidationError,
)

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)
from backend.project.notifications.models import (
    CHANNEL_CHOICES,
    NotificationEvent,
    NotificationRule,
    NotificationTemplate,
)


class NotificationRecipientMatrix(
    BaseMatrix,
):

    class Meta:

        code = "notification-recipient"

        capabilities = {
            "view":
                "notifications.rules.view",

            "edit":
                "notifications.rules.edit",
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

        events = list(
            NotificationEvent.objects
            .filter(
                is_active=True,
            )
            .order_by(
                "group",
                "name",
            )
        )

        channel_options = {
            code: []
            for code, _ in CHANNEL_CHOICES
        }

        for template in templates:

            for channel in (
                template.channels
                or []
            ):
                channel_options.setdefault(
                    channel,
                    [],
                ).append({
                    "value":
                        template.pk,

                    "label":
                        template.name,
                })

        return {
            "layoutRows": [
                {
                    "id":
                        str(event.pk),

                    "label":
                        event.name,
                }
                for event in events
            ],

            "layoutColumns": [
                {
                    "id":
                        code,

                    "label":
                        label,
                }
                for code, label
                in CHANNEL_CHOICES
            ],

            "defaultCell": {
                "widget":
                    "select",
            },

            "columnSchema": {
                code: {
                    "widget":
                        "select",

                    "options":
                        channel_options.get(
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
        recipient = self.get_param(
            request,
            "recipient",
        )

        if not recipient:

            return {
                "items": [],
            }

        recipient_type, recipient_value = (
            self.parse_recipient(
                recipient,
            )
        )

        qs = (
            NotificationRule.objects
            .filter(
                event__isnull=False,
            )
            .select_related(
                "event",
                "template",
            )
        )

        if recipient_type == "role":

            qs = qs.filter(
                role_id=recipient_value,
                logical_role__isnull=True,
            )

        elif recipient_type == "logical":

            qs = qs.filter(
                role__isnull=True,
                logical_role=recipient_value,
            )

        return {
            "items": [
                {
                    "row":
                        str(rule.event_id),

                    "column":
                        rule.channel,

                    "value":
                        rule.template_id,
                }
                for rule in qs
            ],
        }

    # =====================================================
    # SAVE
    # =====================================================

    def save_changes(
        self,
        request,
        changes,
    ):
        recipient = self.get_param(
            request,
            "recipient",
        )

        if not recipient:

            raise ValidationError(
                "Получатель не выбран"
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

            # Новый frontend отправляет x/y.
            # row/column поддерживаются для совместимости.
            row = (
                change.get(
                    "row",
                )
                or change.get(
                    "y",
                )
            )

            column = (
                change.get(
                    "column",
                )
                or change.get(
                    "x",
                )
            )

            event_id = self.parse_event_id(
                row,
            )

            if not column:

                raise ValidationError(
                    "Не указан канал уведомления"
                )

            column = str(
                column,
            ).strip()

            if column not in allowed_channels:

                raise ValidationError(
                    (
                        "Неизвестный канал "
                        f"уведомления: {column}"
                    )
                )

            value = change.get(
                "value",
            )

            # Select может возвращать простой ID
            # либо объект с value/id.
            if isinstance(
                value,
                dict,
            ):
                if "value" in value:

                    value = value.get(
                        "value",
                    )

                else:

                    value = value.get(
                        "id",
                    )

            lookup = {
                "event_id":
                    event_id,

                "channel":
                    column,
            }

            if recipient_type == "role":

                lookup.update({
                    "role_id":
                        recipient_value,

                    "logical_role":
                        None,
                })

            elif recipient_type == "logical":

                lookup.update({
                    "role_id":
                        None,

                    "logical_role":
                        recipient_value,
                })

            # Очистка ячейки удаляет правило.
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
                    "ticket_status":
                        None,

                    "template":
                        template,

                    "enabled":
                        True,
                },
            )

        return {
            "success": True,
        }

    # =====================================================
    # RECIPIENT
    # =====================================================

    def parse_recipient(
        self,
        recipient,
    ):
        recipient = str(
            recipient,
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
                    raw_value,
                )

            except (
                TypeError,
                ValueError,
            ) as exc:

                raise ValidationError(
                    (
                        "Некорректный идентификатор "
                        f"роли: {raw_value}"
                    )
                ) from exc

            if role_id <= 0:

                raise ValidationError(
                    "Некорректный идентификатор роли"
                )

            return (
                "role",
                role_id,
            )

        if recipient.startswith(
            "logical:",
        ):
            logical_role = (
                recipient.split(
                    ":",
                    1,
                )[1]
                .strip()
            )

            if not logical_role:

                raise ValidationError(
                    (
                        "Логическая роль "
                        "не указана"
                    )
                )

            return (
                "logical",
                logical_role,
            )

        raise ValidationError(
            (
                "Неизвестный получатель: "
                f"{recipient}"
            )
        )

    # =====================================================
    # EVENT
    # =====================================================

    def parse_event_id(
        self,
        value,
    ):
        if value in (
            None,
            "",
        ):

            raise ValidationError(
                "Событие не указано"
            )

        try:
            event_id = int(
                value,
            )

        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValidationError(
                (
                    "Некорректный идентификатор "
                    f"события: {value}"
                )
            ) from exc

        event_exists = (
            NotificationEvent.objects
            .filter(
                pk=event_id,
                is_active=True,
            )
            .exists()
        )

        if not event_exists:

            raise ValidationError(
                (
                    "Активное событие "
                    f"#{event_id} не найдено"
                )
            )

        return event_id

    # =====================================================
    # TEMPLATE
    # =====================================================

    def get_template(
        self,
        template_id,
        channel,
    ):
        try:
            template_id = int(
                template_id,
            )

        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValidationError(
                (
                    "Некорректный идентификатор "
                    f"шаблона: {template_id}"
                )
            ) from exc

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
                (
                    "Активный шаблон "
                    f"#{template_id} не найден"
                )
            )

        template_channels = (
            template.channels
            or []
        )

        if channel not in template_channels:

            raise ValidationError(
                (
                    f"Шаблон «{template.name}» "
                    f"не поддерживает канал "
                    f"«{channel}»"
                )
            )

        return template