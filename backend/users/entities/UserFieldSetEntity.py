from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.users.models import (
    UserFieldSet
)


class UserFieldSetEntity(BaseEntity):

    model = UserFieldSet

    entity = "user-fieldsets"

    list_display = [
        "code",
        "name",
        "is_active",
        "is_default",
        "order",
    ]

    search_fields = [
        "code",
        "name",
    ]

    filter_fields = [
        "is_active",
        "is_default",
    ]