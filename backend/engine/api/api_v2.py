# core/api/api_v2.py

import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from backend.engine.api.ApiResolver import api_resolver


# =========================
# BUILD
# =========================

@require_GET
def api_build(request, code: str):

    ctx = {}

    # ctx из query
    raw_ctx = request.GET.get("ctx")
    if raw_ctx:
        try:
            ctx = json.loads(raw_ctx)
        except Exception:
            ctx = {}

    # fallback (для форм)
    if "mode" in request.GET:
        ctx["mode"] = request.GET.get("mode")

    if "id" in request.GET:
        ctx["id"] = request.GET.get("id")

    handler = api_resolver.resolve(code)

    if not hasattr(handler, "build"):
        return JsonResponse(
            {"error": "Handler has no build()"},
            status=400
        )

    result = handler.build(request, ctx)

    return JsonResponse(result)


# =========================
# SUBMIT
# =========================

@require_POST
def api_submit(request, code: str):

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

    handler = api_resolver.resolve(code)

    if not hasattr(handler, "submit"):
        return JsonResponse(
            {"error": "Handler has no submit()"},
            status=400
        )

    result = handler.submit(request, payload, ctx)

    status = 200 if result.get("status") == "ok" else 400

    return JsonResponse(result, status=status)