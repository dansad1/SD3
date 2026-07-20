from pathlib import Path

from django.core.exceptions import ValidationError

from backend.engine.action.Base.BaseAction import BaseAction
from backend.generic.models import StoredFile


class FileUploadAction(BaseAction):

    code = "files.upload"
    permission = None

    max_file_size = 20 * 1024 * 1024

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf",
        ".txt",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
    }

    def run(
        self,
        request,
        payload,
        ctx,
    ):
        uploaded_files = request.FILES.getlist(
            "files",
        )

        if not uploaded_files:
            uploaded = request.FILES.get(
                "file",
            )

            if uploaded:
                uploaded_files = [
                    uploaded,
                ]

        if not uploaded_files:
            return {
                "status": "error",
                "errors": {
                    "__all__": [
                        "Файл не передан",
                    ],
                },
                "debug": {
                    "content_type": getattr(
                        request,
                        "content_type",
                        "",
                    ),
                    "file_keys": list(
                        request.FILES.keys()
                    ),
                },
            }

        result = []

        for uploaded in uploaded_files:
            self.validate_file(
                uploaded,
            )

            obj = StoredFile.objects.create(
                file=uploaded,
                original_name=uploaded.name,
                mime_type=getattr(
                    uploaded,
                    "content_type",
                    "",
                ),
                size=uploaded.size,
                uploaded_by=(
                    request.user
                    if request.user.is_authenticated
                    else None
                ),
            )

            result.append(
                {
                    "id": obj.pk,
                    "name": obj.original_name,
                    "size": obj.size,
                    "mime_type": obj.mime_type,
                    "url": obj.file.url,
                }
            )

        return {
            "status": "ok",
            "files": result,
        }

    def validate_file(
        self,
        uploaded,
    ):
        if uploaded.size > self.max_file_size:
            raise ValidationError(
                "Размер файла превышает 20 МБ",
            )

        extension = Path(
            uploaded.name,
        ).suffix.lower()

        if extension not in self.allowed_extensions:
            raise ValidationError(
                "Недопустимый тип файла",
            )