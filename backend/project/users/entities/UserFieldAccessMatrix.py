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

            "rows": [

                {
                    "id": role.id,
                    "label": str(role),
                }

                for role in UserRole.objects.order_by(
                    "id"
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

    def load_data(self, request):

        field_id = self.get_param(
            request,
            "field",
        )

        if not field_id:
            raise RuntimeError(
                "field param required"
            )

        field = UserField.objects.get(
            pk=field_id
        )

        accesses = {

            access.role_id:
                access.access_level

            for access in (

                UserFieldAccess.objects

                .filter(
                    field=field
                )

            )

        }

        items = []

        for role in UserRole.objects.order_by(
            "id"
        ):

            level = accesses.get(

                role.id,

                UserFieldAccess.ACCESS_NONE,

            )

            items.append({

                "row":
                    role.id,

                "column":
                    "view",

                "value":

                    level in (

                        UserFieldAccess.ACCESS_VIEW,

                        UserFieldAccess.ACCESS_EDIT,

                    ),

            })

            items.append({

                "row":
                    role.id,

                "column":
                    "edit",

                "value":

                    level ==

                    UserFieldAccess.ACCESS_EDIT,

            })

        return {

            "items":
                items,

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

                "field param required"

            )

        field = UserField.objects.get(

            pk=field_id

        )

        accesses = {

            access.role_id:
                access.access_level

            for access in (

                UserFieldAccess.objects

                .filter(
                    field=field
                )

            )

        }

        state = {}

        #
        # текущее состояние из БД
        #

        for role in UserRole.objects.order_by(

                "id"

        ):

            level = accesses.get(

                role.id,

                UserFieldAccess.ACCESS_NONE,

            )

            state[role.id] = {

                "view":

                    level in (

                        UserFieldAccess.ACCESS_VIEW,

                        UserFieldAccess.ACCESS_EDIT,

                    ),

                "edit":

                    level ==

                    UserFieldAccess.ACCESS_EDIT,

            }

        #
        # накладываем изменения
        #

        for change in changes:

            role_id = int(

                change.get("row")

                or

                change.get("y")

            )

            column = (

                change.get("column")

                or

                change.get("x")

            )

            value = change.get(

                "value"

            )

            if isinstance(

                    value,

                    dict,

            ):

                value = value.get(

                    "value"

                )

            state.setdefault(

                role_id,

                {}

            )[column] = bool(

                value

            )

        #
        # сохраняем
        #

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
                    pk=role_id
                )
                raise RuntimeError(
                    f"Роль '{role}' "
                    f"не может иметь "
                    f"право редактирования "
                    f"без права просмотра"
                )
            if can_edit:
                access_level = (
                    UserFieldAccess.ACCESS_EDIT
                )
            elif can_view:
                access_level = (
                    UserFieldAccess.ACCESS_VIEW
                )
            else:
                access_level = (
                    UserFieldAccess.ACCESS_NONE
                )
            access, _ = (
                UserFieldAccess.objects
                .get_or_create(
                    field=field,
                    role_id=role_id,
                    defaults={

                        "access_level":

                            UserFieldAccess.ACCESS_NONE,

                    },

                )

            )

            access.access_level = (

                access_level

            )

            access.save(
                update_fields=[
                    "access_level",
                ]
            )
        return {
            "success":
                True,

        }