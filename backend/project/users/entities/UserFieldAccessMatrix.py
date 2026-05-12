from django.db import transaction

from backend.engine.matrix.Base.BaseMatrix import BaseMatrix
from backend.project.users.models import (
    UserField,
    UserFieldAccess,
    UserRole,
)



class UserFieldAccessMatrix(BaseMatrix):

    class Meta:

        code = "user-field.access"

        capabilities = {
            "view": "user_fields.edit",
            "edit": "user_fields.edit",
        }

    # =====================================================
    # SCHEMA
    # =====================================================

    def build_schema(self, request):

        return {
            "columns": [

                {
                    "key": "role",
                    "label": "Роль",
                    "readonly": True,
                    "width": 320,
                },

                {
                    "key": "access_level",
                    "label": "Доступ",

                    "type": "select",

                    "choices": [
                        {
                            "value": "none",
                            "label": "❌ Нет доступа",
                        },

                        {
                            "value": "view",
                            "label": "👁 Просмотр",
                        },

                        {
                            "value": "edit",
                            "label": "✏️ Редактирование",
                        },
                    ],

                    "width": 240,
                },
            ]
        }

    # =====================================================
    # DATA
    # =====================================================

    def load_data(self, request):

        field_id = request.GET.get("field")

        if not field_id:
            raise RuntimeError(
                "field param required"
            )

        field = UserField.objects.get(
            pk=field_id
        )

        roles = list(
            UserRole.objects
            .all()
            .order_by("id")
        )

        accesses = {
            access.role_id: access
            for access in (
                UserFieldAccess.objects
                .filter(field=field)
                .select_related("role")
            )
        }

        rows = []

        for role in roles:

            access = accesses.get(role.id)

            rows.append({

                "id": role.id,

                "role_id": role.id,

                "role": str(role),

                "access_level": (
                    access.access_level
                    if access
                    else UserFieldAccess.ACCESS_NONE
                ),
            })

        return {
            "rows": rows,

            "meta": {
                "field": {
                    "id": field.id,
                    "name": field.name,
                    "label": field.label,
                }
            }
        }

    # =====================================================
    # SAVE
    # =====================================================

    @transaction.atomic
    def save_changes(
        self,
        request,
        changes: list
    ):

        field_id = request.data.get("field")

        if not field_id:
            raise RuntimeError(
                "field param required"
            )

        field = UserField.objects.get(
            pk=field_id
        )

        allowed_levels = {
            UserFieldAccess.ACCESS_NONE,
            UserFieldAccess.ACCESS_VIEW,
            UserFieldAccess.ACCESS_EDIT,
        }

        for change in changes:

            role_id = change["id"]

            access_level = (
                change.get("access_level")
                or UserFieldAccess.ACCESS_NONE
            )

            if access_level not in allowed_levels:
                raise RuntimeError(
                    f"Invalid access level: "
                    f"{access_level}"
                )

            access, _ = (
                UserFieldAccess.objects.get_or_create(
                    field=field,
                    role_id=role_id,
                    defaults={
                        "access_level": (
                            UserFieldAccess.ACCESS_NONE
                        )
                    }
                )
            )

            access.access_level = access_level

            access.save(
                update_fields=["access_level"]
            )

        return {
            "status": "ok"
        }