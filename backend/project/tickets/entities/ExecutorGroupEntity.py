from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.tickets.models import (
    ExecutorGroup,
)


class ExecutorGroupEntity(
    BaseEntity
):

    model = ExecutorGroup

    entity = "executor-groups"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "name",

        "is_active",

        "created_at",
    ]

    search_fields = [
        "name",
    ]

    filter_fields = [
        "is_active",
    ]

    ordering = [
        "name",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "executor_groups.view",

        "view":
            "executor_groups.view",

        "create":
            "executor_groups.create",

        "edit":
            "executor_groups.edit",

        "delete":
            "executor_groups.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_prefetch_related(self):

        return [
            "companies",
            "users",
        ]