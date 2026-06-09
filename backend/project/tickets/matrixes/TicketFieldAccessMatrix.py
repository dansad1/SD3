# backend/project/tickets/matrixes/TicketFieldAccessMatrix.py

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)

from backend.project.tickets.models import (
    TicketField,
    TicketFieldAccess,
)

from backend.project.users.models import (
    UserRole,
)


class TicketFieldAccessMatrix(
    BaseMatrix
):

    class Meta:

        code = "ticket-field-access"

        capabilities = {

            "view":
                "ticket_fields.view",

            "edit":
                "ticket_fields.edit",
        }

    # =====================================================
    # SCHEMA
    # =====================================================

    def build_schema(
        self,
        request,
    ):
        fields = list(

            TicketField.objects

            .select_related(
                "fieldset",
            )

            .order_by(
                "fieldset__name",
                "order",
                "id",
            )
        )

        roles = list(
            UserRole.objects.order_by(
                "name",
            )
        )

        return {

            "value_type":
                "select",

            "choices": [

                {
                    "value": "none",
                    "label": "Нет доступа",
                },

                {
                    "value": "view",
                    "label": "Просмотр",
                },

                {
                    "value": "edit",
                    "label": "Редактирование",
                },
            ],

            "rows": [

                {
                    "id": field.id,

                    "label":
                        field.label,

                    "group":
                        str(
                            field.fieldset
                        ),
                }

                for field in fields
            ],

            "columns": [

                {
                    "id": role.id,

                    "label":
                        role.name,
                }

                for role in roles
            ],
        }

    # =====================================================
    # DATA
    # =====================================================

    def load_data(
        self,
        request,
    ):
        items = []

        for access in (

            TicketFieldAccess.objects

            .select_related(
                "field",
                "role",
            )
        ):

            items.append({

                "row":
                    access.field_id,

                "column":
                    access.role_id,

                "value":
                    access.access_level,
            })

        return {
            "items": items,
        }

    # =====================================================
    # SAVE
    # =====================================================

    def save_changes(
        self,
        request,
        changes,
    ):
        for change in changes:

            field_id = change["row"]

            role_id = change["column"]

            value = (
                change.get("value")
                or "none"
            )

            access, _ = (

                TicketFieldAccess.objects

                .get_or_create(

                    field_id=field_id,

                    role_id=role_id,
                )
            )

            access.access_level = value

            access.save(
                update_fields=[
                    "access_level",
                ]
            )

        return {
            "success": True,
        }