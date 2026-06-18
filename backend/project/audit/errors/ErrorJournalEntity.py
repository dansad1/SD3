from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.audit.models import (
    ErrorJournal,
)


class ErrorJournalEntity(BaseEntity):

    model = ErrorJournal

    entity = "error-journal"
    capabilities = {
        "list": "audit.view_errorjournal",
        "view": "audit.view_errorjournal",

    }

    ordering = [

        "-created",

    ]

    list_display = [
        "created",
        "exception",
        "user",
        "path",

    ]

    search_fields = [
        "exception",
        "message",
        "path",

    ]

    filter_fields = [
        "resolved",

    ]

    include_fields = {
        "created",
        "user",
        "exception",
        "message",
        "traceback",
        "path",
        "method",
        "ip",
        "resolved",
        "meta",

    }