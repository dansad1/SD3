from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.companies.models import (
    CompanyField,
    Department,
)
from backend.project.companies.services.DepartmentFieldService import DepartmentFieldService

from backend.project.companies.services.DepartmentHierarchyService import (
    DepartmentHierarchyService,
)
from backend.project.companies.services.DepartmentValidationService import (
    DepartmentValidationService,
)


class DepartmentEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = Department

    entity = "department"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "name",
        "company",
        "parent",
        "created_at",
    ]

    search_fields = [
        "name",
    ]

    filter_fields = [
        "company",
        "parent",
        "archived",
    ]

    ordering = [
        "name",
    ]

    hierarchy = True

    hierarchy_parent_field = "parent"

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "departments.view",
        "view": "departments.view",
        "create": "departments.create",
        "edit": "departments.edit",
        "delete": "departments.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):

        return [
            "company",
            "parent",
        ]

    def get_prefetch_related(
        self,
    ):

        return [
            "children",
            "users",
        ]

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
            self,
            request,
            obj=None,
    ):
        return DepartmentFieldService.get_fields(
            request=request,
            department=obj,
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
            "label": obj.get_full_path(),
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

        DepartmentValidationService.validate(
            payload=payload,
            instance=instance,
        )

        return payload

    # =====================================================
    # BEFORE SAVE
    # =====================================================

    def before_save(
        self,
        ctx,
    ):

        ctx = super().before_save(
            ctx,
        )

        DepartmentHierarchyService.before_save(
            ctx,
        )

        return ctx

    # =====================================================
    # TREE
    # =====================================================

    def serialize_hierarchy_meta(
        self,
        obj,
    ):

        return (
            DepartmentHierarchyService
            .serialize_meta(
                obj,
            )
        )

    # =====================================================
    # DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        super().before_delete(
            request,
            instance,
        )

        instance.users.clear()

        return None