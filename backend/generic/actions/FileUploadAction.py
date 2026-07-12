from django.core.files.base import File

from backend.engine.action.Base.BaseAction import BaseAction
from backend.generic.models import StoredFile


class FileUploadAction(BaseAction):

    code = "files.upload"

    permission = None

    def run(
        self,
        request,
        payload,
        ctx,
    ):

        uploaded = request.FILES.get("files")

        if not uploaded:

            uploaded = request.FILES.get("file")

        if not uploaded:

            return {
                "status": "error",
                "errors": {
                    "__all__": [
                        "Файл не передан",
                    ],
                },
            }

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

        return {

            "status": "ok",

            "files": [

                {

                    "id": obj.pk,

                    "name": obj.original_name,

                    "size": obj.size,

                    "mime_type": obj.mime_type,

                    "url": obj.file.url,

                }

            ],

        }