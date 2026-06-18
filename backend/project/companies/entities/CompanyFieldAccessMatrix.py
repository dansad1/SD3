from django.db import transaction

from backend.engine.matrix.Base.BaseMatrix import BaseMatrix
from backend.project.companies.models import (
    CompanyField,
    CompanyFieldAccess,
)
from backend.project.users.models import UserRole


class CompanyFieldAccessMatrix(BaseMatrix):

    class Meta:
        code = "company-field.access"

        capabilities = {
            "view": "company_fields.edit",
            "edit": "company_fields.edit",
        }

    def build_schema(self, request):
        return {
            "rows": [
                {
                    "id": role.id,
                    "label": str(role),
                }
                for role in UserRole.objects.order_by("id")
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

    def load_data(self, request):
        field_id = self.get_param(request, "field")

        if not field_id:
            raise RuntimeError("field param required")

        field = CompanyField.objects.get(pk=field_id)

        accesses = {
            access.role_id: access.access_level
            for access in CompanyFieldAccess.objects.filter(field=field)
        }

        items = []

        for role in UserRole.objects.order_by("id"):
            level = accesses.get(
                role.id,
                CompanyFieldAccess.ACCESS_NONE,
            )

            items.append({
                "row": role.id,
                "column": "view",
                "value": level in (
                    CompanyFieldAccess.ACCESS_VIEW,
                    CompanyFieldAccess.ACCESS_EDIT,
                ),
            })

            items.append({
                "row": role.id,
                "column": "edit",
                "value": level == CompanyFieldAccess.ACCESS_EDIT,
            })

        return {
            "items": items,
        }

    @transaction.atomic
    def save_changes(self, request, changes):
        field_id = self.get_param(request, "field")

        if not field_id:
            raise RuntimeError("field param required")

        field = CompanyField.objects.get(pk=field_id)

        accesses = {
            access.role_id: access.access_level
            for access in CompanyFieldAccess.objects.filter(field=field)
        }

        state = {}

        for role in UserRole.objects.order_by("id"):
            level = accesses.get(
                role.id,
                CompanyFieldAccess.ACCESS_NONE,
            )

            state[role.id] = {
                "view": level in (
                    CompanyFieldAccess.ACCESS_VIEW,
                    CompanyFieldAccess.ACCESS_EDIT,
                ),
                "edit": level == CompanyFieldAccess.ACCESS_EDIT,
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

            value = change.get("value")

            if isinstance(value, dict):
                value = value.get("value")

            state.setdefault(role_id, {})[column] = bool(value)

        for role_id, values in state.items():
            can_view = values.get("view", False)
            can_edit = values.get("edit", False)

            if can_edit and not can_view:
                role = UserRole.objects.get(pk=role_id)

                raise RuntimeError(
                    f"Роль '{role}' не может иметь "
                    f"право редактирования без права просмотра"
                )

            if can_edit:
                access_level = CompanyFieldAccess.ACCESS_EDIT
            elif can_view:
                access_level = CompanyFieldAccess.ACCESS_VIEW
            else:
                access_level = CompanyFieldAccess.ACCESS_NONE

            access, _ = CompanyFieldAccess.objects.get_or_create(
                field=field,
                role_id=role_id,
                defaults={
                    "access_level": CompanyFieldAccess.ACCESS_NONE,
                },
            )

            access.access_level = access_level
            access.save(update_fields=["access_level"])

        return {
            "success": True,
        }