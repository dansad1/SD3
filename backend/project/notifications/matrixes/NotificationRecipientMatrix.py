# backend/project/notifications/matrixes/NotificationRecipientMatrix.py

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)

from backend.project.notifications.models import (
    NotificationRule,
    NotificationEvent,
    NotificationTemplate,
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
                "channel",
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

        return {

            "value_type":
                "select",

            "choices": [

                {
                    "value":
                        template.id,

                    "label":
                        (
                            f"{template.channel}"
                            f" / "
                            f"{template.name}"
                        ),
                }

                for template in templates
            ],

            "rows": [

                {
                    "id":
                        event.id,

                    "label":
                        event.name,
                }

                for event in events
            ],

            "columns": [

                {
                    "id":
                        "template",

                    "label":
                        "Шаблон",
                }
            ],
        }

    def load_data(
        self,
        request,
    ):
        recipient = request.GET.get(
            "recipient"
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
            "role:"
        ):

            role_id = int(
                recipient.split(
                    ":",
                    1,
                )[1]
            )

            qs = qs.filter(
                role_id=role_id,
            )

        elif recipient.startswith(
            "logical:"
        ):

            logical_role = (
                recipient.split(
                    ":",
                    1,
                )[1]
            )

            qs = qs.filter(
                logical_role=
                logical_role,
            )

        return {

            "items": [

                {
                    "row":
                        rule.event_id,

                    "column":
                        "template",

                    "value":
                        rule.template_id,
                }

                for rule in qs
            ]
        }

    def save_changes(
        self,
        request,
        changes,
    ):
        recipient = request.GET.get(
            "recipient"
        )

        if not recipient:
            return {
                "success": False,
            }

        for change in changes:

            event_id = change["row"]

            template_id = change.get(
                "value"
            )

            defaults = {

                "template_id":
                    template_id,

                "enabled":
                    True,
            }

            if recipient.startswith(
                "role:"
            ):

                role_id = int(
                    recipient.split(
                        ":",
                        1,
                    )[1]
                )

                NotificationRule.objects.update_or_create(

                    event_id=event_id,

                    role_id=role_id,

                    defaults=defaults,
                )

            elif recipient.startswith(
                "logical:"
            ):

                logical_role = (
                    recipient.split(
                        ":",
                        1,
                    )[1]
                )

                NotificationRule.objects.update_or_create(

                    event_id=event_id,

                    logical_role=
                        logical_role,

                    defaults=defaults,
                )

        return {
            "success": True,
        }