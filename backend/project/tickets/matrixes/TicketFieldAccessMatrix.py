from django.db import transaction

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


class TicketFieldAccessMatrix(BaseMatrix):

    class Meta:

        code = "ticket-field.access"

        capabilities = {
            "view": "ticket_fields.edit",
            "edit": "ticket_fields.edit",
        }

    # =====================================================
    # SCHEMA
    # =====================================================

    def build_schema(
        self,
        request,
    ):

        return {
            "rows": [
                {
                    "id": role.id,
                    "label": str(role),
                }
                for role in (
                    UserRole.objects
                    .order_by("name")
                )
            ],
            "columns": [
                {
                    "id": "view",
                    "label": "👁 Просмотр",
                },
                {
                    "id": "edit",
                    "label": "✏️ Редактирование",
                },
            ],
            "defaultCell": {
                "widget": "checkbox",
            },
        }

    # =====================================================
    # DATA
    # =====================================================

    def load_data(
        self,
        request,
    ):

        field_id = self.get_param(
            request,
            "field",
        )

        if not field_id:
            raise RuntimeError(
                "field param required",
            )

        field = TicketField.objects.get(
            pk=field_id,
        )

        accesses = {
            access.role_id: access.access_level
            for access in (
                TicketFieldAccess.objects
                .filter(field=field)
            )
        }

        items = []

        for role in (
            UserRole.objects
            .order_by("name")
        ):

            level = accesses.get(role.id)

            items.extend([
                {
                    "row": role.id,
                    "column": "view",
                    "value": level in (
                        TicketFieldAccess.ACCESS_VIEW,
                        TicketFieldAccess.ACCESS_EDIT,
                    ),
                },
                {
                    "row": role.id,
                    "column": "edit",
                    "value": (
                        level ==
                        TicketFieldAccess.ACCESS_EDIT
                    ),
                },
            ])

        return {
            "items": items,
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

        field_id = self.get_param(
            request,
            "field",
        )

        if not field_id:
            raise RuntimeError(
                "field param required",
            )

        field = TicketField.objects.get(
            pk=field_id,
        )

        accesses = {
            access.role_id: access.access_level
            for access in (
                TicketFieldAccess.objects
                .filter(field=field)
            )
        }

        state = {}

        # =================================================
        # CURRENT STATE
        # =================================================

        for role in (
            UserRole.objects
            .order_by("name")
        ):

            level = accesses.get(role.id)

            state[role.id] = {
                "view": level in (
                    TicketFieldAccess.ACCESS_VIEW,
                    TicketFieldAccess.ACCESS_EDIT,
                ),
                "edit": (
                    level ==
                    TicketFieldAccess.ACCESS_EDIT
                ),
            }

        # =================================================
        # APPLY CHANGES
        # =================================================

        for change in changes:

            role_id = int(
                change.get("row")
                or change.get("y")
            )

            column = (
                change.get("column")
                or change.get("x")
            )

            value = change.get("value")

            if isinstance(value, dict):
                value = value.get("value")

            state.setdefault(
                role_id,
                {},
            )[column] = bool(value)

        # =================================================
        # SAVE
        # =================================================

        for role_id, values in state.items():

            can_view = values.get(
                "view",
                False,
            )

            can_edit = values.get(
                "edit",
                False,
            )

            if can_edit and not can_view:

                role = UserRole.objects.get(
                    pk=role_id,
                )

                raise RuntimeError(
                    f"Роль '{role}' не может иметь "
                    f"право редактирования без "
                    f"права просмотра"
                )

            # ---------------------------------------------
            # Нет прав -> удаляем запись
            # ---------------------------------------------

            if not can_view:

                TicketFieldAccess.objects.filter(
                    field=field,
                    role_id=role_id,
                ).delete()

                continue

            # ---------------------------------------------
            # Определяем уровень
            # ---------------------------------------------

            access_level = (
                TicketFieldAccess.ACCESS_EDIT
                if can_edit
                else TicketFieldAccess.ACCESS_VIEW
            )

            access, _ = (
                TicketFieldAccess.objects
                .get_or_create(
                    field=field,
                    role_id=role_id,
                    defaults={
                        "access_level": access_level,
                    },
                )
            )

            if access.access_level != access_level:

                access.access_level = access_level

                access.save(
                    update_fields=[
                        "access_level",
                    ]
                )

        return {
            "success": True,
        }