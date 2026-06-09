# backend/project/notifications/matrixes/NotificationStatusMatrix.py

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)

from backend.project.notifications.models import (
    NotificationRule,
    NotificationTemplate,
)

from backend.project.tickets.models import (
    TicketStatus,
)


class NotificationStatusMatrix(
    BaseMatrix
):

    class Meta:

        code = "notification-status"

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
                "channel",
                "name",
            )
        )

        statuses = list(

            TicketStatus.objects

            .order_by(
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
                        status.id,

                    "label":
                        status.name,
                }

                for status in statuses
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

    # =====================================================
    # DATA
    # =====================================================

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
                ticket_status__isnull=False,
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
                        rule.ticket_status_id,

                    "column":
                        "template",

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
        recipient = request.GET.get(
            "recipient"
        )

        if not recipient:

            return {
                "success": False,
            }

        for change in changes:

            status_id = change["row"]

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

                    ticket_status_id=status_id,

                    role_id=role_id,

                    event=None,

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

                    ticket_status_id=status_id,

                    logical_role=
                        logical_role,

                    event=None,

                    defaults=defaults,
                )

        return {
            "success": True,
        }