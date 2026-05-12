from rest_framework.exceptions import PermissionDenied

from backend.engine.matrix.Base.MatrixContext import MatrixContext
from backend.engine.matrix.Base.changes import extract_changes
from backend.engine.matrix.Base.data import load_data
from backend.engine.matrix.Base.save import save
from backend.engine.matrix.Base.schema import build_schema
from backend.engine.utils.permissions import has_permission


# =========================
# PERMISSION
# =========================

def build_capabilities(ctx: MatrixContext):
    matrix = ctx.matrix
    request = ctx.request

    actions = ["view", "edit"]

    ctx.capabilities = {
        action: has_permission(
            type("PermCtx", (), {
                "request": request,
                "entity": type("EntityStub", (), {
                    "capabilities": {
                        action: matrix.capabilities.get(action)
                    }
                })()
            }),
            action
        )
        for action in actions
    }


def check_permission(ctx: MatrixContext, action: str):
    matrix = ctx.matrix
    request = ctx.request

    perm_code = matrix.capabilities.get(action)

    # 🔥 если permission не задан — просто считаем доступным
    if not perm_code:
        return

    perm_ctx = type("PermCtx", (), {})()
    perm_ctx.request = request
    perm_ctx.entity = type("EntityStub", (), {})()

    perm_ctx.entity.capabilities = {
        action: perm_code
    }

    if not has_permission(perm_ctx, action):
        raise PermissionDenied


# =========================
# PIPELINES
# =========================

BUILD_PIPELINE = [
    build_capabilities,          # 🔥 ВСЕГДА первым
    lambda ctx: check_permission(ctx, "view"),
    load_data,
    build_schema,
]

SUBMIT_PIPELINE = [
    build_capabilities,          # 🔥 тоже здесь
    lambda ctx: check_permission(ctx, "edit"),
    extract_changes,
    save,
]


# =========================
# BASE MATRIX
# =========================

class BaseMatrix:

    class Meta:
        code: str | None = None
        capabilities: dict | None = None

    def __init__(self):
        meta = getattr(self, "Meta", None)

        if not meta or not getattr(meta, "code", None):
            raise RuntimeError(
                f"{self.__class__.__name__} must define Meta.code"
            )

        self.code = meta.code
        self.capabilities = getattr(meta, "capabilities", {}) or {}

    # -------------------------
    # ABSTRACT
    # -------------------------

    def build_schema(self, request):
        raise NotImplementedError

    def load_data(self, request):
        raise NotImplementedError

    def save_changes(self, request, changes: list):
        raise NotImplementedError

    # -------------------------
    # BUILD
    # -------------------------

    def build(self, request):

        ctx = MatrixContext(
            matrix=self,
            request=request
        )

        for step in BUILD_PIPELINE:
            step(ctx)

        return {
            **(ctx.data or {}),
            "schema": ctx.schema,
            "capabilities": ctx.capabilities,  # ✅ всегда есть
        }

    # -------------------------
    # SUBMIT
    # -------------------------

    def submit(self, request, payload: dict):

        ctx = MatrixContext(
            matrix=self,
            request=request,
            payload=payload
        )

        for step in SUBMIT_PIPELINE:
            step(ctx)

        return ctx.result