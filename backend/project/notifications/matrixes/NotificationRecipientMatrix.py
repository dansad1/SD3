from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)


from backend.project.notifications.models import (
    NotificationEvent,
    NotificationRule,
    NotificationTemplate, CHANNEL_CHOICES,
)


class NotificationRecipientMatrix(
    BaseMatrix
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
                ).append(

                    {
                        "value":
                            template.pk,

                        "label":
                            template.name,
                    }

                )

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

                for code, _
                in CHANNEL_CHOICES

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

        qs = (

            NotificationRule.objects

            .filter(
                event__isnull=False,
            )

        )

        if recipient.startswith(
            "role:",
        ):

            qs = qs.filter(

                role_id=int(
                    recipient.split(
                        ":",
                        1,
                    )[1]
                )

            )

        elif recipient.startswith(
            "logical:",
        ):

            qs = qs.filter(

                logical_role=recipient.split(
                    ":",
                    1,
                )[1]

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

            ]

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

            return {

                "success":
                    False,

            }

        for change in changes:

            event_id = int(
                change["row"],
            )

            channel = change[
                "column"
            ]

            template_id = change.get(
                "value",
            )

            defaults = {

                "template_id":
                    template_id,

                "enabled":
                    True,

            }

            if recipient.startswith(
                "role:",
            ):

                NotificationRule.objects.update_or_create(

                    event_id=event_id,

                    role_id=int(
                        recipient.split(
                            ":",
                            1,
                        )[1]
                    ),

                    channel=channel,

                    defaults=defaults,

                )

            elif recipient.startswith(
                "logical:",
            ):

                NotificationRule.objects.update_or_create(

                    event_id=event_id,

                    logical_role=recipient.split(
                        ":",
                        1,
                    )[1],

                    channel=channel,

                    defaults=defaults,

                )

        return {

            "success":
                True,

        }