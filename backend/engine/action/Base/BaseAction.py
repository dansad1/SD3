from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from backend.engine.action.Base.ActionContext import (
    ActionContext,
)

from backend.engine.action.Base.ActionField import (
    ActionField,
)

from backend.engine.action.Base.execute import (
    execute,
)

from backend.engine.action.Base.lifecycle import (
    after,
    before,
)

from backend.engine.action.Base.validate import (
    validate,
)

from backend.engine.form.Base.errors import (
    validation_error_to_dict,
)

from backend.engine.utils.permissions import (
    has_permission,
)


# =========================================================
# PERMISSION
# =========================================================

def check_permission(
    ctx: ActionContext
):

    action = ctx.action

    request = ctx.request

    if not action.permission:
        return ctx

    perm_ctx = type(
        "PermCtx",
        (),
        {},
    )()

    perm_ctx.request = request

    perm_ctx.entity = type(
        "EntityStub",
        (),
        {},
    )()

    perm_ctx.entity.capabilities = {
        "run": action.permission
    }

    if not has_permission(
        perm_ctx,
        "run",
    ):

        raise PermissionDenied

    return ctx


# =========================================================
# LOAD RUNTIME FIELDS
# =========================================================

def load_runtime_fields(
    ctx: ActionContext
):

    runtime_fields = []

    for config in ctx.action.get_fields(
        ctx.request,
        ctx.ctx,
    ):

        runtime_fields.append(
            ActionField(config)
        )

    ctx.runtime_fields = (
        runtime_fields
    )

    ctx.field_map = {

        field.name: field

        for field in (
            runtime_fields
        )
    }

    return ctx


# =========================================================
# BUILD SCHEMA
# =========================================================

def build_schema(
    ctx: ActionContext
):

    fields = []

    for field in (
        ctx.runtime_fields
        or []
    ):

        schema = (
            field.get_schema()
        )

        print(
            "[ACTION FIELD]",
            field.name,
            schema,
        )

        fields.append(
            schema
        )

    ctx.fields = fields

    return ctx


# =========================================================
# PIPELINE
# =========================================================

PIPELINE = [

    check_permission,

    load_runtime_fields,

    validate,

    before,

    execute,

    after,
]


# =========================================================
# BASE ACTION
# =========================================================

class BaseAction:

    code = ""

    permission = None

    confirm = None

    success_message = None

    # =====================================================
    # CONTEXT
    # =====================================================

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

    # =====================================================
    # FIELDS
    # =====================================================

    def get_fields(
        self,
        request,
        ctx,
    ):

        return []

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        request,
        ctx,
    ):

        action_ctx = self.ctx(

            request,

            ctx=ctx,
        )

        check_permission(
            action_ctx
        )

        load_runtime_fields(
            action_ctx
        )

        build_schema(
            action_ctx
        )

        return {

            "fields":
                action_ctx.fields,

            "initial": {},

            "confirm":
                self.confirm,
        }

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        request,
        payload,
        ctx,
    ):

        return payload

    # =====================================================
    # EXECUTION
    # =====================================================

    def run(
        self,
        request,
        payload,
        ctx,
    ):

        return {
            "status": "ok"
        }

    # =====================================================
    # LIFECYCLE
    # =====================================================

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

    # =====================================================
    # SUBMIT
    # =====================================================

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

                "errors":
                    validation_error_to_dict(
                        e
                    ),
            }

        except Exception as e:

            return {

                "status": "error",

                "errors": {
                    "__all__": [
                        str(e)
                    ]
                },
            }

        return action_ctx.result