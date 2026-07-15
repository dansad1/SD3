from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)
from backend.project.users.services.UserAfterSaveService import UserAfterSaveService
from backend.project.users.services.UserDeleteService import UserDeleteService
from backend.project.users.services.UserFieldAccessService import UserFieldAccessService
from backend.project.users.services.UserFieldService import UserFieldService
from backend.project.users.services.UserPasswordService import UserPasswordService

from backend.project.users.models import (
    User,
)
from backend.project.users.services.UserSchemaService import UserSchemaService


class UserEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = User

    entity = "user"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "login",
        "role",
        "is_active",
        "telegram",
        "department",
        "company",
        "full_name",
    ]

    search_fields = [
        "login",
        "telegram",
        "company",
        "full_name",
    ]

    filter_fields = [
        "role",
        "is_active",
    ]

    ordering = [
        "login",
    ]

    exclude_fields = {
        "groups",
        "user_permissions",
        "last_login",
        "created_at",
        "updated_at",
        "fieldset",
    }

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "users.view",
        "view": "users.view",
        "create": "users.create",
        "edit": "users.edit",
        "delete": "users.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(
        self,
    ):
        return [
            "role",
            "fieldset",
        ]

    def get_prefetch_related(
        self,
    ):
        return [
            "dynamic_values",
            "dynamic_values__field",
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
            UserFieldAccessService
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
            UserFieldService
            .get_fields()
        )

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):
        UserPasswordService.validate(
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

        UserPasswordService.apply(
            instance=ctx.instance,
            payload=ctx.data,
        )

        return ctx

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

        UserAfterSaveService.process(
            ctx,
        )

        return ctx

    # =====================================================
    # BEFORE DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):
        UserDeleteService.validate(
            actor=request.user,
            target=instance,
        )

        super().before_delete(
            request,
            instance,
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
        return UserSchemaService.customize(
            request=request,
            schema=schema,
        )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent_option(
        self,
        obj,
    ):
        return {
            "value": obj.pk,
            "label": (
                obj.get_value(
                    "full_name",
                )
                or obj.login
            ),
        }