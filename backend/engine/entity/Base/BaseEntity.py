from rest_framework.exceptions import (
    PermissionDenied,
)

from backend.engine.change.ChangeDetector import ChangeDetector
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
from backend.project.audit.utils.logging import log_entity_event, serialize_instance, make_json_safe


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

    filter_exclude_fields = set()
    # =====================================================
    # FORM
    # =====================================================

    form_sections = None

    def get_form_sections(
            self,
            request,
            obj=None,
    ):
        return self.form_sections

    def get_filter_fields(
            self,
            request,
            obj=None,
    ):

        excluded = set(

            self.filter_exclude_fields

            or []

        )

        return [

            field

            for field in self.get_fields(

                request,

                obj=obj,

            )

            if (

                    field.name

                    and

                    field.name

                    not in excluded

            )

        ]

    # =====================================================
    # FIELD POLICY
    # =====================================================

    include_fields = None

    exclude_fields = None

    system_exclude_fields = {
        "id",
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

            for action in (
                    self.capabilities
                    or {}
            ).keys()
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

        access_map = {}

        access_method = getattr(
            self,
            "get_field_access_map",
            None,
        )

        if access_method:
            access_map = (
                    access_method(
                        request,
                        obj=obj,
                    )
                    or {}
            )

        # =================================================
        # DJANGO FIELDS
        # =================================================

        for field in (
                self.model._meta.get_fields()
        ):

            name = getattr(
                field,
                "name",
                None,
            )

            if not name:
                continue

            if not self.include_model_field(
                    field
            ):
                continue

            fields.append(
                DjangoField(
                    field
                )
            )

        # =================================================
        # DYNAMIC FIELDS
        # =================================================

        for field in self.get_dynamic_fields(
                request,
                obj=obj,
        ):

            runtime = DynamicField(
                field,
            )

            if access_map:

                access = access_map.get(
                    field.name,
                )

                if not access:
                    continue

                if access == "view":
                    runtime.readonly = True

            fields.append(
                runtime,
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
    def serialize_for_audit(
            self,
            request,
            instance,
    ):
        if not instance:
            return {}

        data = {}

        for field in self.get_fields(
                request=request,
                obj=instance,
        ):
            try:
                data[field.name] = make_json_safe(
                    field.get_audit_value(
                        instance,
                    )
                )
            except Exception:
                continue

        return data
    def before_save(
            self,
            ctx,
    ):
        instance = getattr(
            ctx,
            "instance",
            None,
        )

        if instance and instance.pk:
            ctx.before_state = self.serialize_for_audit(
                request=ctx.request,
                instance=instance,
            )
        else:
            ctx.before_state = {}

        ctx.changes = []

        return ctx

    def after_save(
            self,
            ctx,
    ):
        instance = getattr(
            ctx,
            "instance",
            None,
        )

        if not instance:
            return ctx

        ctx.after_state = self.serialize_for_audit(
            request=ctx.request,
            instance=instance,
        )

        ctx.changes = ChangeDetector().detect_from_state(
            entity=self,
            before=ctx.before_state,
            after=ctx.after_state,
        )

        action = (
            "create"
            if ctx.mode == "create"
            else "update"
        )

        log_entity_event(
            request=ctx.request,
            action=action,
            entity=self.entity,
            instance=instance,
            before=ctx.before_state,
            after=ctx.after_state,
            meta={
                "mode": ctx.mode,
                "entity": self.entity,
                "changes": ctx.changes.to_list(),
            },
        )

        return ctx

    def before_delete(
            self,
            request,
            instance,
    ):
        instance._audit_before_delete = {
            "state": self.serialize_for_audit(
                request=request,
                instance=instance,
            ),
            "id": instance.pk,
            "repr": str(instance),
        }

    def after_delete(
            self,
            request,
            instance,
    ):

        audit = getattr(
            instance,
            "_audit_before_delete",
            {},
        )

        log_entity_event(

            request=request,

            action="delete",

            entity=self.entity,

            instance=instance,

            before=audit.get(
                "state",
                {},
            ),

            after={},

            meta={

                "entity":
                    self.entity,

                "object_id":
                    audit.get(
                        "id"
                    ),

                "object_repr":
                    audit.get(
                        "repr"
                    ),

            },

        )
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

    def customize_field_schema(
            self,
            field,
            schema,
            request=None,
            obj=None,
    ):
        return schema


