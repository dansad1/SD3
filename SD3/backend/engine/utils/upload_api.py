# core/api/upload_api.py

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.conf import settings
import mimetypes



MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]


@require_POST
def upload_api(request):

    if not request.user.is_authenticated:
        raise PermissionDenied

    files = request.FILES.getlist("file")

    if not files:
        return JsonResponse({"error": "No files provided"}, status=400)

    results = []

    for file in files:

        # 🔐 size limit
        if file.size > MAX_FILE_SIZE:
            return JsonResponse({
                "error": f"{file.name} exceeds size limit"
            }, status=400)

        # 🔐 mime check
        mime_type, _ = mimetypes.guess_type(file.name)
        if mime_type not in ALLOWED_TYPES:
            return JsonResponse({
                "error": f"{file.name} has invalid type"
            }, status=400)

        upload = Upload.objects.create(
            file=file,
            original_name=file.name,
            uploaded_by=request.user,
            entity=request.POST.get("entity"),
            object_id=request.POST.get("object_id"),
        )

        results.append({
            "id": upload.id,
            "url": upload.file.url,
            "name": upload.original_name,
            "size": file.size,
        })

    return JsonResponse({"files": results})