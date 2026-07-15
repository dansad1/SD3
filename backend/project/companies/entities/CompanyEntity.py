from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.companies.models import (
    Company,
)
from backend.project.companies.services.CompanyAfterSaveService import (
    CompanyAfterSaveService,
)
from backend.project.companies.services.CompanyFieldAccessService import (
    CompanyFieldAccessService,
)
from backend.project.companies.services.CompanyFieldService import (
    CompanyFieldService,
)
from backend.project.companies.services.CompanySchemaService import (
    CompanySchemaService,
)
from backend.project.companies.services.CompanyValidationService import (
    CompanyValidationService,
)


class CompanyEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = Company

    entity = "company"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "archived",
        "created_at",
        "name",
        "phone",
        "email",
        "company",
    ]

    search_fields = [
        "name",
        "phone",
        "email",
    ]

    filter_fields = [
        "archived",
        "company",
    ]

    ordering = [
        "-created_at",
    ]

    exclude_fields = [
        "fieldset",
        "created_at",
        "updated_at",
        "choices",
        "options",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "companies.view",
        "view": "companies.view",
        "create": "companies.create",
        "edit": "companies.edit",
        "delete": "companies.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):
        return [
            "fieldset",
        ]

    def get_prefetch_related(
        self,
    ):
        return [
            "dynamic_values",
        ]

    # =====================================================
    # FIELD ACCESS
    # =====================================================

    def get_field_access_map(
        self,
        request,
        obj=None,
    ):
        return (
            CompanyFieldAccessService
            .get_access_map(
                request,
            )
        )

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):
        return (
            CompanyFieldService
            .get_fields(
                request=request,
                company=obj,
            )
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def represent_option(
        self,
        obj,
    ):
        return {
            "value": obj.pk,
            "label": (
                obj.get_value(
                    "name",
                )
                or f"Company #{obj.pk}"
            ),
        }

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):
        CompanyValidationService.validate(
            payload,
        )

        return payload

    # =====================================================
    # AFTER SAVE
    # =====================================================

    def after_save(
        self,
        ctx,
    ):
        ctx = super().after_save(
            ctx,
        )

        CompanyAfterSaveService.process(
            ctx,
        )

        return ctx

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):
        return (
            CompanySchemaService
            .customize(
                request=request,
                schema=schema,
            )
        )

    # =====================================================
    # FILTERS
    # =====================================================

    def apply_queryset_filters(
        self,
        request,
        qs,
    ):
        qs = super().apply_queryset_filters(
            request,
            qs,
        )

        service = request.GET.get(
            "services",
        )

        if service:

            qs = qs.filter(
                services=service,
            )

        return qs