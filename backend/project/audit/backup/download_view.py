from pathlib import Path
from types import SimpleNamespace

from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.engine.utils.permissions import has_permission


BACKUP_DIR = Path(settings.BASE_DIR) / "backups"

ALLOWED_FILES = {
    "db.sqlite3",
    "media.zip",
}


def can_download_backup(request):
    permission_context = SimpleNamespace(
        request=request,
        entity=SimpleNamespace(
            capabilities={
                "download": "view_backups",
            },
        ),
    )

    return has_permission(
        permission_context,
        "download",
    )


class BackupDownloadView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        backup_id,
        filename,
    ):
        if filename not in ALLOWED_FILES:
            raise Http404

        if not can_download_backup(request):
            raise Http404

        backup_root = BACKUP_DIR.resolve()

        file_path = (
            backup_root
            / str(backup_id)
            / filename
        ).resolve()

        try:
            file_path.relative_to(
                backup_root
            )
        except ValueError as exc:
            raise Http404 from exc

        if not file_path.is_file():
            raise Http404

        return FileResponse(
            file_path.open("rb"),
            as_attachment=True,
            filename=filename,
        )