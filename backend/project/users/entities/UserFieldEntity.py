from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.project.users.models import UserField


class UserFieldEntity(BaseEntity):

    model = UserField

    entity = "user-fields"

    list_display = [
        "fieldset",
        "name",
        "label",
        "field_type",
        "required",
        "readonly",
        "hidden",
        "order",
    ]

    search_fields = [
        "name",
        "label",
    ]

    filter_fields = [
        "fieldset",
        "field_type",
    ]

    ordering = [
        "fieldset",
        "order",
        "id",
    ]

    capabilities = {
        "list": "user_fields.view",
        "view": "user_fields.view",
        "create": "user_fields.create",
        "edit": "user_fields.edit",
        "delete": "user_fields.delete",
    }

    def get_select_related(self):

        return [
            "fieldset",
        ]