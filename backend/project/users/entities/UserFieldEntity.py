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
    # FORM
    # =====================================================

    form_sections = [

        (
            "Основное",
            [
                "fieldset",
                "name",
                "label",
                "field_type",
            ],
        ),

        (
            "UI",
            [
                "placeholder",
                "help_text",
                "default_value",
                "choices",
            ],
        ),

        (
            "Валидация",
            [
                "required",
                "unique",
                "regex",
                "min_value",
                "max_value",
            ],
        ),

        (
            "Системное",
            [
                "is_multiple",
                "is_system",
            ],
        ),
    ]

    # =====================================================
    # LIST
    # =====================================================

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