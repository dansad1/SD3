from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError

from SD3.backend.engine.entity.Base.lifecycle import before_save, after_save
from SD3.backend.engine.entity.Base.permissions import has_permission
from SD3.backend.engine.entity.EntityRegistry import entity_registry
from SD3.backend.engine.form.Base.FormContext import FormContext
from SD3.backend.engine.form.Base.errors import validation_error_to_dict
from SD3.backend.engine.form.Base.initial import apply_query_initial
from SD3.backend.engine.form.Base.instance import load_instance
from SD3.backend.engine.form.Base.normalize import normalize
from SD3.backend.engine.form.Base.save import save
from SD3.backend.engine.form.Base.save_dynamic import save_dynamic
from SD3.backend.engine.form.Base.schema import build_schema
from SD3.backend.engine.form.Base.serialize import serialize


# =========================
# DEBUG WRAPPER
# =========================

def debug_step(name, fn):
    def wrapped(ctx):
        print(f"\n===== 🔷 STEP: {name} =====")
        print("mode:", ctx.mode)
        print("pk:", ctx.pk)

        print("payload:", getattr(ctx, "payload", None))

        before = getattr(ctx, "data", None)
        print("data BEFORE:", before)

        result = fn(ctx)

        after = getattr(ctx, "data", None)
        print("data AFTER:", after)

        if hasattr(ctx, "fields"):
            print("fields:", [f["name"] for f in (ctx.fields or [])])

        if hasattr(ctx, "instance"):
            print("instance:", ctx.instance)

        return result

    wrapped.__name__ = fn.__name__
    return wrapped


# =========================
# PAYLOAD
# =========================

def apply_payload(ctx: FormContext):
    """
    payload → ctx.data
    """
    ctx.data = (ctx.payload or {}).copy()
    return ctx


# =========================
# SECURITY (🔥 КРИТИЧНО)
# =========================

def filter_allowed_fields(ctx: FormContext):
    """
    whitelist по schema
    """
    allowed = {f["name"] for f in ctx.fields}

    ctx.data = {
        k: v for k, v in (ctx.data or {}).items()
        if k in allowed
    }

    return ctx


def filter_readonly_fields(ctx: FormContext):
    """
    нельзя менять readonly
    """
    readonly = {
        f["name"]
        for f in ctx.fields
        if f.get("readonly")
    }

    ctx.data = {
        k: v for k, v in ctx.data.items()
        if k not in readonly
    }

    return ctx


# =========================
# PERMISSION
# =========================

def check_permission(ctx: FormContext):
    entity = ctx.entity
    request = ctx.request

    action_map = {
        "view": "view",
        "create": "create",
        "edit": "edit",
    }

    action = action_map.get(ctx.mode)

    if not action:
        raise PermissionDenied

    if not has_permission(entity.ctx(request), action):
        raise PermissionDenied

    ctx.capabilities = entity.get_capabilities_for_user(request)


# =========================
# PIPELINES
# =========================

BUILD_PIPELINE = [
    debug_step("check_permission", check_permission),
    debug_step("load_instance", load_instance),
    debug_step("build_schema", build_schema),
    debug_step("serialize", serialize),
    debug_step("apply_query_initial", apply_query_initial),
]

SUBMIT_PIPELINE = [
    debug_step("check_permission", check_permission),
    debug_step("load_instance", load_instance),
    debug_step("build_schema", build_schema),

    # 🔥 payload
    debug_step("apply_payload", apply_payload),

    # 🔥 безопасность
    debug_step("filter_allowed_fields", filter_allowed_fields),
    debug_step("filter_readonly_fields", filter_readonly_fields),

    # 🔥 нормализация
    debug_step("normalize", normalize),

    # 🔥 hooks
    debug_step("before_save", before_save),

    # 🔥 django save
    debug_step("save", save),

    # 🔥 dynamic save
    debug_step("save_dynamic", save_dynamic),

    # 🔥 after
    debug_step("after_save", after_save),
]


# =========================
# BASE FORM
# =========================

class BaseForm:
    code = None
    entity = None

    # -------------------------
    # ENTITY
    # -------------------------

    def get_entity(self):
        if self.entity:
            return self.entity

        entity_name = self.code.split(".")[0]
        return entity_registry.get(entity_name)

    def resolve_pk(self, request, mode, pk):
        entity = self.get_entity()

        if hasattr(entity, "resolve_pk"):
            return entity.resolve_pk(request, mode, pk)

        return pk

    # -------------------------
    # BUILD
    # -------------------------

    def build(self, request, mode, pk=None):
        print("\n\n🚀 ===== BUILD FORM START =====")

        pk = self.resolve_pk(request, mode, pk)

        if pk and mode == "create":
            print("⚠️ FIX MODE: create → edit")
            mode = "edit"

        ctx = FormContext(
            form=self,
            request=request,
            mode=mode,
            pk=pk,
        )

        for step in BUILD_PIPELINE:
            step(ctx)

        print("✅ FINAL INITIAL:", ctx.data)
        print("🚀 ===== BUILD FORM END =====\n\n")

        return {
            "entity": ctx.entity.entity,
            "fields": ctx.fields,
            "initial": ctx.data,
            "capabilities": ctx.capabilities,
        }

    # -------------------------
    # SUBMIT
    # -------------------------

    @transaction.atomic
    def submit(self, request, mode, payload, pk=None):
        print("\n\n🚀 ===== SUBMIT FORM START =====")

        if mode == "view":
            raise PermissionDenied

        pk = self.resolve_pk(request, mode, pk)

        ctx = FormContext(
            form=self,
            request=request,
            mode=mode,
            pk=pk,
            payload=payload,
        )

        try:
            for step in SUBMIT_PIPELINE:
                step(ctx)

        except ValidationError as e:
            print("❌ VALIDATION ERROR:", e)
            return {
                "status": "error",
                "errors": validation_error_to_dict(e),
            }

        except Exception as e:
            print("💥 UNKNOWN ERROR:", e)
            return {
                "status": "error",
                "errors": {"__all__": [str(e)]},
            }

        print("✅ SAVE OK, ID:", ctx.instance.pk)
        print("🚀 ===== SUBMIT FORM END =====\n\n")

        return {
            "status": "ok",
            "id": ctx.instance.pk,
        }