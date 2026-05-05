import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import ValidationError

from .MatrixRegistry import matrix_registry


@require_GET
def matrix_api(request, code):
    try:
        matrix = matrix_registry.get(code)
        return JsonResponse(matrix.build(request))

    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_POST
def matrix_submit_api(request, code):
    try:
        matrix = matrix_registry.get(code)

        payload = json.loads(request.body.decode() or "{}")

        return JsonResponse(matrix.submit(request, payload))

    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)