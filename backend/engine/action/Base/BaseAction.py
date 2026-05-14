from rest_framework.exceptions import PermissionDenied, ValidationError

from backend.engine.action.Base.ActionContext import ActionContext
from backend.engine.action.Base.ActionField import ActionField
from backend.engine.action.Base.execute import execute
from backend.engine.action.Base.lifecycle import after, before
from backend.engine.action.Base.validate import validate
from backend.engine.form.Base.errors import validation_error_to_dict

from backend.engine.schema.context import FieldContext
from backend.engine.schema.types import step_detect_type
from backend.engine.schema.widgets import step_widget

from backend.engine.utils.permissions import has_permission


# =========================
# PERMISSION
# =========================

def check_permission(ctx: ActionContext):

    action = ctx.action
    request = ctx.request

    if not action.permission:
        return

    perm_ctx = type("PermCtx", (), {})()

    perm_ctx.request = request
    perm_ctx.entity = type("EntityStub", (), {})()

    perm_ctx.entity.capabilities = {
        "run": action.permission
    }

    if not has_permission(perm_ctx, "run"):
        raise PermissionDenied


# =========================
# FIELD PIPELINE
# =========================

FIELD_PIPELINE = [
    step_detect_type,
    step_widget,
]


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

    permission = None

    confirm = None
    success_message = None

    # -------------------------
    # CONTEXT
    # -------------------------

    def ctx(
        self,
        request,
        ctx=None,
        payload=None,
    ):
        return ActionContext(
            action=self,
            request=request,
            ctx=ctx,
            payload=payload,
        )

    # -------------------------
    # SCHEMA
    # -------------------------

    def get_fields(
        self,
        request,
        ctx,
    ):
        return []

    def build(
        self,
        request,
        ctx,
    ):

        action_ctx = self.ctx(
            request,
            ctx=ctx,
        )

        check_permission(action_ctx)

        fields = []

        for field in self.get_fields(request, ctx):

            adapted = ActionField(field)

            field_ctx = FieldContext(
                model=None,
                field=adapted,
                entity=None,
                request=request,
                action="edit",
            )

            # raw schema
            field_ctx.schema.update(field)

            # unified pipeline
            for step in FIELD_PIPELINE:
                step(field_ctx)

            print(
                "[ACTION FIELD]",
                field_ctx.name,
                field_ctx.schema
            )

            fields.append(field_ctx.schema)

        action_ctx.fields = fields

        return {
            "fields": action_ctx.fields,
            "initial": {},
            "confirm": self.confirm,
        }

    # -------------------------
    # HOOKS
    # -------------------------

    def validate(
        self,
        request,
        payload,
        ctx,
    ):
        return payload

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        return {
            "status": "ok"
        }

    def before(
        self,
        request,
        payload,
        ctx,
    ):
        pass

    def after(
        self,
        request,
        result,
        ctx,
    ):
        pass

    # -------------------------
    # EXECUTION
    # -------------------------
    def submit(
            self,
            request,
            payload,
            ctx,
    ):

        action_ctx = self.ctx(
            request,
            ctx=ctx,
            payload=payload,
        )

        try:
            for step in PIPELINE:
                step(action_ctx)

        except ValidationError as e:
            return {
                "status": "error",
                "errors": validation_error_to_dict(e),
            }

        except Exception as e:
            return {
                "status": "error",
                "errors": {
                    "__all__": [str(e)]
                },
            }

        return action_ctx.result