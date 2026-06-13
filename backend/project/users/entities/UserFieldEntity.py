from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.users.models import (
    UserField,
)


class UserFieldEntity(BaseEntity):

    model = UserField

    entity = "user-fields"

    # =====================================================
    # LIST
    # =====================================================

    list_display = [
        "name",
        "label",
        "field_type",
        "required",
        "unique",
        "is_system",
    ]

    search_fields = [
        "name",
        "label",
    ]

    filter_fields = [
        "field_type",
    ]

    # =====================================================
    # PERMISSIONS
    # =====================================================

    capabilities = {
        "list": "user_fields.view",
        "view": "user_fields.view",
        "create": "user_fields.create",
        "edit": "user_fields.edit",
        "delete": "user_fields.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "fieldset",
        ]

    # =====================================================
    # FORM
    # =====================================================

    exclude_fields = [

        "fieldset",


    ]