from django.db import transaction

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)
from backend.project.users.models import (
    UserRole,
)


class BaseFieldAccessMatrix(BaseMatrix):

    field_model = None
    access_model = None

    role_order = "id"

    # =====================================================
    # HELPERS
    # =====================================================

    def get_field(self, request):

        field_id = self.get_param(
            request,
            "field",
        )

        if not field_id:
            raise RuntimeError(
                "field param required",
            )

        return self.field_model.objects.get(
            pk=field_id,
        )

    def get_roles(self):

        return (
            UserRole.objects
            .order_by(self.role_order)
        )

    def get_accesses(self, field):

        return {
            access.role_id: access.access_level
            for access in (
                self.access_model.objects
                .filter(field=field)
            )
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
                for role in self.get_roles()
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

        field = self.get_field(
            request,
        )

        accesses = self.get_accesses(
            field,
        )

        items = []

        for role in self.get_roles():

            level = accesses.get(
                role.id,
            )

            items.extend([
                {
                    "row": role.id,
                    "column": "view",
                    "value": level in (
                        self.access_model.ACCESS_VIEW,
                        self.access_model.ACCESS_EDIT,
                    ),
                },
                {
                    "row": role.id,
                    "column": "edit",
                    "value": (
                        level ==
                        self.access_model.ACCESS_EDIT
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

        field = self.get_field(
            request,
        )

        accesses = self.get_accesses(
            field,
        )

        state = {}

        for role in self.get_roles():

            level = accesses.get(
                role.id,
            )

            state[role.id] = {
                "view": level in (
                    self.access_model.ACCESS_VIEW,
                    self.access_model.ACCESS_EDIT,
                ),
                "edit": (
                    level ==
                    self.access_model.ACCESS_EDIT
                ),
            }

        for change in changes:

            role_id = int(
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
                value = value.get(
                    "value",
                )

            state.setdefault(
                role_id,
                {},
            )[column] = bool(value)

        for role_id, values in state.items():

            can_view = values.get(
                "view",
                False,
            )

            can_edit = values.get(
                "edit",
                False,
            )

            if (
                can_edit
                and not can_view
            ):

                role = UserRole.objects.get(
                    pk=role_id,
                )

                raise RuntimeError(
                    f"Роль '{role}' "
                    f"не может иметь "
                    f"право "
                    f"редактирования "
                    f"без просмотра"
                )

            if not can_view:

                self.access_model.objects.filter(
                    field=field,
                    role_id=role_id,
                ).delete()

                continue

            access_level = (
                self.access_model.ACCESS_EDIT
                if can_edit
                else self.access_model.ACCESS_VIEW
            )

            self.access_model.objects.update_or_create(
                field=field,
                role_id=role_id,
                defaults={
                    "access_level": access_level,
                },
            )

        return {
            "success": True,
        }