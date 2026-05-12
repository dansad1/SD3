# core/api/action/api.py

import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from backend.engine.action.ActionRegistry import actions


@require_GET
def action_form_api(request, code: str):

    ctx = json.loads(request.GET.get("ctx", "{}"))

    action = actions.get(code)

    result = action.build(request, ctx)

    return JsonResponse({
        "layout": "simple",
        "fields": result["fields"],
        "initial": result.get("initial", {}),
        "confirm": result.get("confirm"),
    })


@require_POST
def action_submit_api(request, code):

    # ctx + payload
    if request.content_type.startswith("multipart/"):
        payload = request.POST.dict()
        raw_ctx = payload.pop("_ctx", None)

        try:
            ctx = json.loads(raw_ctx) if raw_ctx else {}
        except Exception:
            ctx = {}
    else:
        payload = json.loads(request.body or "{}")
        ctx = payload.pop("_ctx", {})

    action = actions.get(code)

    result = action.submit(request, payload, ctx)

    return JsonResponse(result)