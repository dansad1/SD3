# core/api/generics/FormApi.py

import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from SD3.backend.engine.form.FormRegistry import form_registry


@require_GET
def entity_form_api(request, entity: str):

    mode = request.GET.get("mode", "create")
    pk = request.GET.get("id")

    form = form_registry.get(f"{entity}.form")

    result = form.build(request, mode, pk)

    return JsonResponse({
        "layout": "simple",
        "fields": result["fields"],
        "initial": result["initial"],
        "capabilities": result.get("capabilities", {}),
    })


@require_POST
def entity_form_submit_api(request, entity: str):

    mode = request.GET.get("mode", "create")
    pk = request.GET.get("id")

    payload = json.loads(request.body or "{}")

    form = form_registry.get(f"{entity}.form")

    # 🔥 ВСЕГДА есть submit
    result = form.submit(request, mode, payload, pk)

    status = 200 if result.get("status") == "ok" else 400

    return JsonResponse(result, status=status)