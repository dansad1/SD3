from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.audit.models import AuthJournal


class AuthJournalEntity(BaseEntity):

    model = AuthJournal

    entity = "auth-journal"

    capabilities = {

        "list": "audit.view_authjournal",

        "view": "audit.view_authjournal",
    }

    ordering = [
        "-created",
    ]

    list_display = [

        "created",

        "user",

        "action",

        "ip",
    ]

    search_fields = [

        "user__username",

        "ip",
    ]

    filter_fields = [

        "action",
    ]

    include_fields = {

        "created",

        "user",

        "action",

        "ip",

        "user_agent",

        "meta",
    }