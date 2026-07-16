from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.services.models import (
    Service,
)

from backend.project.services.services.ServiceAfterSaveService import (
    ServiceAfterSaveService,
)
from backend.project.services.services.ServiceHierarchyService import (
    ServiceHierarchyService,
)
from backend.project.services.services.ServiceSchemaService import (
    ServiceSchemaService,
)
from backend.project.services.services.ServiceValidationService import (
    ServiceValidationService,
)


class ServiceEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = Service

    entity = "service"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "name",
        "code",
        "parent",
        "owner",
        "schedule",
        "created_at",
    ]

    search_fields = [
        "name",
        "code",
        "description",
    ]

    filter_fields = [
        "parent",
        "owner",
        "schedule",
        "companies",
        "ticket_types",
        "ticket_categories",
        "roles",
        "archived",
    ]

    ordering = [
        "name",
    ]

    # =====================================================
    # TREE
    # =====================================================

    hierarchy = True

    hierarchy_parent_field = "parent"

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "services.view",
        "view": "services.view",
        "create": "services.create",
        "edit": "services.edit",
        "delete": "services.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):
        return [
            "parent",
            "owner",
            "schedule",
        ]

    def get_prefetch_related(
        self,
    ):
        return [
            "children",
            "users",
            "companies",
            "roles",
            "ticket_types",
            "ticket_categories",
        ]

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
        return ServiceValidationService.validate(
            payload=payload,
            instance=instance,
        )

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

        return ServiceHierarchyService.before_save(
            ctx,
        )

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

        return ServiceAfterSaveService.process(
            ctx,
        )

    # =====================================================
    # TREE META
    # =====================================================

    def serialize_hierarchy_meta(
        self,
        obj,
    ):
        return ServiceHierarchyService.serialize_meta(
            obj,
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):
        return ServiceSchemaService.customize(
            request=request,
            schema=schema,
            field=field,
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
        instance.companies.clear()
        instance.roles.clear()
        instance.ticket_types.clear()
        instance.ticket_categories.clear()

        return None