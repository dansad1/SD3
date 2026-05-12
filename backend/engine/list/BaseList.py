from django.core.exceptions import PermissionDenied

from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.list.Base.ListContext import ListContext
from backend.engine.list.Base.fields import build_fields
from backend.engine.list.Base.filters import apply_filters
from backend.engine.list.Base.pagination import paginate
from backend.engine.list.Base.queryset import load_queryset
from backend.engine.list.Base.search import apply_search
from backend.engine.list.Base.serialize import serialize
from backend.engine.list.Base.sort import apply_sort
from backend.engine.list.Base.visibility import apply_visibility
from backend.engine.utils.permissions import has_permission


def check_permission(ctx: ListContext):
    entity = ctx.entity
    request = ctx.request

    if not has_permission(entity.ctx(request), "list"):
        raise PermissionDenied

    ctx.capabilities = entity.get_capabilities_for_user(request)


PIPELINE = [
    check_permission,
    load_queryset,
    apply_search,
    apply_filters,
    apply_sort,
    paginate,
    build_fields,
    apply_visibility,
    serialize,
]


class BaseList:
    code = None
    entity = None

    def get_entity(self):
        if self.entity:
            return self.entity

        name = self.code.replace(".list", "")
        return entity_registry.get(name)

    def build(self, request):
        ctx = ListContext(
            list_obj=self,
            request=request,
        )

        for step in PIPELINE:
            step(ctx)

        return {
            "fields": ctx.fields,
            "rows": ctx.rows,
            "meta": {
                "page": ctx.page.number,
                "pages": ctx.paginator.num_pages,
                "total": ctx.paginator.count,
            },
            "capabilities": ctx.capabilities,
        }