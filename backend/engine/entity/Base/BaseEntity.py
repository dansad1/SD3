from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from backend.engine.entity.Base.EntityContext import EntityContext
from backend.engine.entity.Base.options import get_options
from backend.engine.entity.Base.permissions import has_permission
from backend.engine.entity.Base.queryset import get_queryset
from backend.engine.entity.Base.representation import represent

f
class BaseEntity:
    # -------------------------
    # CONFIG
    # -------------------------

    model = None
    entity = ""

    list_display = None
    search_fields = []

    include_fields = None
    exclude_fields = None

    system_exclude_fields = {
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    capabilities = {}
    soft_delete = True

    # -------------------------
    # CONTEXT
    # -------------------------

    def ctx(self, request):
        return EntityContext(entity=self, request=request)

    # -------------------------
    # PERMISSIONS
    # -------------------------

    def check_permission(self, request, action):
        if not has_permission(self.ctx(request), action):
            raise PermissionDenied

    def get_capabilities_for_user(self, request):
        ctx = self.ctx(request)

        return {
            action: has_permission(ctx, action)
            for action in ["list", "view", "create", "edit", "delete"]
        }

    # -------------------------
    # QUERYSET
    # -------------------------

    def get_queryset(self, request):
        return get_queryset(self.ctx(request))

    def apply_user_scope(self, request, qs):
        """
        Переопределяется в entity
        """
        return qs

    # -------------------------
    # REPRESENTATION
    # -------------------------

    def represent(self, obj, field):
        return represent(self, obj, field)

    # -------------------------
    # OPTIONS (Select / FK)
    # -------------------------

    def get_options(self, request):
        return get_options(self.ctx(request))

    # -------------------------
    # FIELD FILTER (Django)
    # -------------------------

    def should_include_field(self, field):
        name = field.name

        if name in self.system_exclude_fields:
            return False

        if field.auto_created and not field.concrete:
            return False

        if getattr(field, "many_to_many", False) and field.auto_created:
            return False

        if self.exclude_fields and name in self.exclude_fields:
            return False

        if self.include_fields is not None:
            return name in self.include_fields

        return True

    # -------------------------
    # FIELD FILTER (Dynamic)
    # -------------------------

    def get_dynamic_fields(self, request):
        """
        Переопределяется в entity (например UserField)
        """
        return []

    def should_include_dynamic_field(self, request, field):
        name = field.name

        if name in self.system_exclude_fields:
            return False

        if self.exclude_fields and name in self.exclude_fields:
            return False

        if self.include_fields is not None:
            return name in self.include_fields

        return True

    # -------------------------
    # LIST POLICY
    # -------------------------

    def should_include_field_name(self, name: str):
        if name in self.system_exclude_fields:
            return False

        if self.exclude_fields and name in self.exclude_fields:
            return False

        if self.include_fields is not None:
            return name in self.include_fields

        return True

    def should_include_in_list(self, name: str):
        return self.should_include_field_name(name)

    # -------------------------
    # LIFECYCLE: SAVE
    # -------------------------

    def before_save(self, ctx):
        return ctx

    def after_save(self, ctx):
        return ctx

    # -------------------------
    # LIFECYCLE: DELETE
    # -------------------------

    def before_delete(self, request, instance):
        pass

    def after_delete(self, request, instance):
        pass

    def perform_delete(self, request, instance):
        if self.soft_delete and hasattr(instance, "deleted_at"):
            instance.deleted_at = timezone.now()
            instance.save(update_fields=["deleted_at"])
        else:
            instance.delete()

    def delete_instance(self, request, instance):
        self.check_permission(request, "delete")

        self.before_delete(request, instance)
        self.perform_delete(request, instance)
        self.after_delete(request, instance)

        return {"status": "ok"}

    # -------------------------
    # SCHEMA HOOK
    # -------------------------

    def customize_field_schema(self, request, schema, field=None):
        """
        Позволяет менять schema на лету
        """
        return schema