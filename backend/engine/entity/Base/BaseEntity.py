from rest_framework.exceptions import (
    PermissionDenied,
)

from backend.engine.entity.Base.EntityContext import (
    EntityContext,
)

from backend.engine.entity.Base.delete import (
    perform_delete,
)

from backend.engine.entity.Base.permissions import (
    has_permission,
)

from backend.engine.entity.Base.queryset import (
    get_queryset,
)

from backend.engine.entity.Base.options import (
    get_options,
)

from backend.engine.entity.Base.representation import (
    represent,
)
from backend.generic.models import DjangoField, DynamicField


class BaseEntity:

    # =====================================================
    # CORE
    # =====================================================

    model = None

    entity = ""

    # =====================================================
    # UI
    # =====================================================

    list_display = []

    search_fields = []

    filter_fields = []

    ordering = ["id"]

    # =====================================================
    # FIELD POLICY
    # =====================================================

    include_fields = None

    exclude_fields = None

    system_exclude_fields = {
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {}

    # =====================================================
    # STORAGE
    # =====================================================

    soft_delete = True

    # =====================================================
    # CONTEXT
    # =====================================================

    def ctx(
        self,
        request,
        **kwargs,
    ):

        return EntityContext(
            entity=self,
            request=request,
            **kwargs,
        )

    # =====================================================
    # PERMISSIONS
    # =====================================================

    def has_permission(
        self,
        request,
        action,
    ):

        return has_permission(
            self.ctx(
                request,
                action=action,
            ),
            action,
        )

    def check_permission(
        self,
        request,
        action,
    ):

        if not self.has_permission(
            request,
            action,
        ):

            raise PermissionDenied

    def get_capabilities_for_user(
        self,
        request,
    ):

        return {

            action: self.has_permission(
                request,
                action,
            )

            for action in [
                "list",
                "view",
                "create",
                "edit",
                "delete",
            ]
        }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_queryset(
        self,
        request,
    ):

        return get_queryset(
            self.ctx(request)
        )

    def apply_user_scope(
        self,
        request,
        qs,
    ):

        return qs

    def get_select_related(self):

        return []

    def get_prefetch_related(self):

        return []

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def represent(
        self,
        obj,
        field,
        mode="list",
    ):

        return represent(

            entity=self,

            obj=obj,

            field=field,

            mode=mode,
        )

    def represent_option(
        self,
        obj,
    ):

        return {
            "value": obj.pk,
            "label": str(obj),
        }

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        request,
    ):

        return get_options(
            self.ctx(request)
        )

    # =====================================================
    # RUNTIME FIELDS
    # =====================================================

    def get_fields(
            self,
            request,
            obj=None,
    ):

        fields = []

        # =================================================
        # DJANGO FIELDS
        # =================================================

        for field in (
                self.model._meta.get_fields()
        ):

            # ---------------------------------------------
            # NAME
            # ---------------------------------------------

            name = getattr(
                field,
                "name",
                None,
            )

            if not name:
                continue

            # ---------------------------------------------
            # INCLUDE
            # ---------------------------------------------

            if not self.include_model_field(
                    field
            ):
                continue

            # ---------------------------------------------
            # DJANGO FIELD
            # ---------------------------------------------

            fields.append(
                DjangoField(field)
            )

        # =================================================
        # DYNAMIC FIELDS
        # =================================================

        for field in self.get_dynamic_fields(
                request,
                obj=obj,
        ):
            fields.append(
                DynamicField(field)
            )

        # =================================================
        # SORT
        # =================================================

        fields.sort(
            key=lambda x: (
                x.order,
                x.name,
            )
        )

        return fields
    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        return []

    # =====================================================
    # FIELD POLICY
    # =====================================================

    def include_model_field(
        self,
        field,
    ):

        name = field.name

        # =================================================
        # INCLUDE LIST
        # =================================================

        if (
            self.include_fields
            and name not in self.include_fields
        ):

            return False

        # =================================================
        # EXCLUDE LIST
        # =================================================

        if (
            self.exclude_fields
            and name in self.exclude_fields
        ):

            return False

        # =================================================
        # SYSTEM
        # =================================================

        if name in self.system_exclude_fields:

            return False

        # =================================================
        # REVERSE RELATIONS
        # =================================================

        if (
            field.auto_created
            and not field.concrete
        ):

            return False

        # =================================================
        # AUTO MANY TO MANY
        # =================================================

        if (
            getattr(
                field,
                "many_to_many",
                False,
            )
            and field.auto_created
        ):

            return False

        return True

    # =====================================================
    # SAVE LIFECYCLE
    # =====================================================

    def before_save(
        self,
        ctx,
    ):

        return ctx

    def after_save(
        self,
        ctx,
    ):

        return ctx

    # =====================================================
    # DELETE LIFECYCLE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        pass

    def after_delete(
        self,
        request,
        instance,
    ):

        pass

    def perform_delete(
        self,
        request,
        instance,
    ):

        return perform_delete(
            self,
            request,
            instance,
        )

    def delete_instance(
        self,
        request,
        instance,
    ):

        self.check_permission(
            request,
            "delete",
        )

        return self.perform_delete(
            request,
            instance,
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

        """
        Entity-level validation hook.
        """

        return payload