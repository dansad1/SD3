from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.users.models import (
    UserField
)


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
        "is_multiple",
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

    def get_queryset(self, request):

        return (
            super()
            .get_queryset(request)
            .select_related(
                "fieldset"
            )
        )
