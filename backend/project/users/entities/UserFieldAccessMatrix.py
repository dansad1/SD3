from backend.project.audit.utils.BaseFieldAccessMatrix import BaseFieldAccessMatrix
from backend.project.users.models import (
    UserField,
    UserFieldAccess,
)


class UserFieldAccessMatrix(
    BaseFieldAccessMatrix,
):

    field_model = UserField

    access_model = UserFieldAccess

    role_order = "id"

    class Meta:

        code = "user-field.access"

        capabilities = {
            "view": "user_fields.edit",
            "edit": "user_fields.edit",
        }