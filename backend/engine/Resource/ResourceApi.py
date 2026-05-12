# core/api/generics/ResourceApi.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from backend.engine.Resource.ResourceRegistry import resource_registry


@require_GET
def resource_api(request, code: str):
    resource = resource_registry.get(code)

    resource.check_permission(request)

    params = request.GET.dict()

    result = resource.get(request, **params)

    return JsonResponse(result, safe=isinstance(result, dict))