from backend.engine.entity.Base.BaseEntity import (
    BaseEntity
)

from backend.project.companies.models import (
    CompanyFieldSet
)


class CompanyFieldSetEntity(BaseEntity):

    model = CompanyFieldSet

    entity = "company-fieldsets"

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

    ordering = [
        "order",
        "id",
    ]

    capabilities = {
        "list": "company_fieldsets.view",
        "view": "company_fieldsets.view",
        "create": "company_fieldsets.create",
        "edit": "company_fieldsets.edit",
        "delete": "company_fieldsets.delete",
    }