# =========================================================
# backend/project/services/entities/ServiceEntity.py
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.services.entities.sync import sync_service

from backend.project.services.models import (
    Service,
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

        "list":
            "services.view",

        "view":
            "services.view",

        "create":
            "services.create",

        "edit":
            "services.edit",

        "delete":
            "services.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "parent",
            "owner",
            "schedule",
        ]

    def get_prefetch_related(self):

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

            "value":
                obj.pk,

            "label":
                obj.get_full_path(),
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

        errors = {}

        # =================================================
        # NAME
        # =================================================

        if not payload.get(
            "name"
        ):

            errors["name"] = [
                "Название обязательно"
            ]

        # =================================================
        # CODE
        # =================================================

        code = payload.get(
            "code"
        )

        if not code:

            errors["code"] = [
                "Код обязателен"
            ]

        else:

            qs = Service.objects.filter(
                code=code
            )

            if instance:

                qs = qs.exclude(
                    pk=instance.pk
                )

            if qs.exists():

                errors["code"] = [
                    "Сервис с таким кодом уже существует"
                ]

        # =================================================
        # SELF PARENT
        # =================================================

        parent = payload.get(
            "parent"
        )

        if (

            instance
            and parent
            and parent.pk == instance.pk

        ):

            errors["parent"] = [
                "Сервис не может быть родителем самому себе"
            ]

        # =================================================
        # CYCLIC TREE
        # =================================================

        if instance and parent:

            current = parent

            while current:

                if current.pk == instance.pk:

                    errors["parent"] = [
                        "Нельзя создать циклическую иерархию"
                    ]

                    break

                current = current.parent

        # =================================================
        # RESULT
        # =================================================

        if errors:

            raise ValidationError(
                errors
            )

        return payload

    # =====================================================
    # TREE META
    # =====================================================

    def serialize_hierarchy_meta(
        self,
        obj,
    ):

        return {

            "_depth":
                self.get_depth(obj),

            "_parent":
                obj.parent_id,

            "_has_children":
                obj.has_children,
        }

    # =====================================================
    # DEPTH
    # =====================================================

    def get_depth(
        self,
        obj,
    ):
        depth = 0
        parent = obj.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):

        # =================================================
        # READONLY
        # =================================================

        if schema["name"] in {

            "id",

            "created_at",

            "updated_at",
        }:

            schema["readonly"] = True

        # =================================================
        # PARENT FILTER
        # =================================================

        if schema["name"] == "parent":

            schema["filter"] = {

                "archived": False,
            }

        # =================================================
        # USERS
        # =================================================

        if schema["name"] == "users":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = "user"

        # =================================================
        # COMPANIES
        # =================================================

        if schema["name"] == "companies":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = "company"

        # =================================================
        # ROLES
        # =================================================

        if schema["name"] == "roles":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = "user_role"

        # =================================================
        # CATEGORIES
        # =================================================

        if schema["name"] == "ticket_categories":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = (
                "ticket_category"
            )

        # =================================================
        # TYPES
        # =================================================

        if schema["name"] == "ticket_types":

            schema["widget"] = (
                "entity_multiselect"
            )

            schema["entity"] = (
                "ticket_type"
            )

        return schema

    # =====================================================
    # DELETE
    # =====================================================
    def after_save(
            self,
            ctx,
    ):
        ctx = super().after_save(
            ctx,
        )

        sync_service(
            ctx.instance,
        )

        return ctx
    def before_delete(
        self,
        request,
        instance,
    ):

        # ================================================
        # DETACH M2M
        # ================================================
        instance.users.clear()
        instance.companies.clear()
        instance.roles.clear()
        instance.ticket_types.clear()
        instance.ticket_categories.clear()

        return None