from rest_framework.exceptions import PermissionDenied

from backend.engine.Resource.ResourceList.ResourceListContext import ResourceListContext
from backend.engine.Resource.ResourceList.fetch import fetch
from backend.engine.Resource.ResourceList.fields import build_fields
from backend.engine.Resource.ResourceList.meta import build_meta
from backend.engine.Resource.ResourceList.rows import extract_rows
from backend.engine.Resource.ResourceRegistry import resource_registry
from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.list.BaseList import BaseList
from backend.engine.utils.permissions import has_permission


def check_permission(ctx: ResourceListContext):
    resource = ctx.list_obj.get_resource()
    request = ctx.request

    if getattr(resource, "entity", None):
        entity = entity_registry.get(resource.entity)

        if not has_permission(entity.ctx(request), "list"):
            raise PermissionDenied

        ctx.capabilities = entity.get_capabilities_for_user(request)
        return

    capabilities = getattr(resource, "capabilities", {}) or {}
    code = capabilities.get("list")

    if not code:
        ctx.capabilities = {"list": True}
        return

    perm_ctx = type("PermCtx", (), {})()
    perm_ctx.request = request
    perm_ctx.entity = type("EntityStub", (), {})()

    perm_ctx.entity.capabilities = {
        "list": code
    }

    if not has_permission(perm_ctx, "list"):
        raise PermissionDenied

    ctx.capabilities = {
        "list": has_permission(perm_ctx, "list")
    }


PIPELINE = [
    check_permission,
    fetch,
    extract_rows,
    build_fields,   # ✅ теперь правильная функция
    build_meta,
]


class ResourceList(BaseList):

    resource = None

    def __init__(self, resource=None, code=None):
        self.resource = resource
        self.code = code or (
            f"{resource.code}.list" if resource else None
        )

    def get_resource(self):
        if self.resource:
            return self.resource


        resource_code = self.code.replace(".list", "")
        return resource_registry.get(resource_code)

    def build(self, request):

        ctx = ResourceListContext(
            list_obj=self,
            request=request
        )

        for step in PIPELINE:
            step(ctx)

        return {
            "fields": ctx.fields,
            "items": ctx.rows,
            "page": ctx.meta,
            "capabilities": ctx.capabilities,
        }