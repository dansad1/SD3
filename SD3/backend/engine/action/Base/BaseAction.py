from rest_framework.exceptions import PermissionDenied

from SD3.backend.engine.action.Base.ActionContext import ActionContext
from SD3.backend.engine.action.Base.execute import execute
from SD3.backend.engine.action.Base.lifecycle import after, before
from SD3.backend.engine.action.Base.validate import validate
from SD3.backend.engine.entity.Base.permissions import has_permission


# =========================
# PERMISSION
# =========================

def check_permission(ctx: ActionContext):
    action = ctx.action
    request = ctx.request

    # если permission не задан — action доступен
    if not action.permission:
        return

    # универсальный permission-контекст
    perm_ctx = type("PermCtx", (), {})()
    perm_ctx.request = request
    perm_ctx.entity = type("EntityStub", (), {})()

    perm_ctx.entity.capabilities = {
        "run": action.permission
    }

    if not has_permission(perm_ctx, "run"):
        raise PermissionDenied


# =========================
# PIPELINE
# =========================

PIPELINE = [
    check_permission,
    validate,
    before,
    execute,
    after,
]


# =========================
# BASE ACTION
# =========================

class BaseAction:

    code = ""
    permission = None   # строка permission-кода
    confirm = None
    success_message = None

    # -------------------------
    # CONTEXT
    # -------------------------

    def ctx(self, request, ctx=None, payload=None):
        return ActionContext(
            action=self,
            request=request,
            ctx=ctx,
            payload=payload,
        )

    # -------------------------
    # SCHEMA (для FormBlock action)
    # -------------------------

    def get_fields(self, request, ctx):
        return []

    def build(self, request, ctx):

        action_ctx = self.ctx(request, ctx=ctx)

        check_permission(action_ctx)

        action_ctx.fields = self.get_fields(request, ctx)

        return {
            "fields": action_ctx.fields,
            "initial": {},
            "confirm": self.confirm,
        }

    # -------------------------
    # HOOKS (переопределяются)
    # -------------------------

    def validate(self, request, payload, ctx):
        return payload

    def run(self, request, payload, ctx):
        return {"status": "ok"}

    def before(self, request, payload, ctx):
        pass

    def after(self, request, result, ctx):
        pass

    # -------------------------
    # EXECUTION
    # -------------------------

    def submit(self, request, payload, ctx):

        action_ctx = self.ctx(
            request,
            ctx=ctx,
            payload=payload
        )

        for step in PIPELINE:
            step(action_ctx)

        return action_ctx.result