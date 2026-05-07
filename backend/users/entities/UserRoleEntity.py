from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.users.models import (
    UserRole
)


class UserRoleEntity(BaseEntity):

    model = UserRole

    entity = "roles"

    list_display = [
        "code",
        "name",
        "is_active",
        "priority",
    ]

    search_fields = [
        "code",
        "name",
    ]

    filter_fields = [
        "is_active",
    ]