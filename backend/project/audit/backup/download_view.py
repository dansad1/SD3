import os
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required


BACKUP_DIR = os.path.join(settings.BASE_DIR, "backups")

ALLOWED_FILES = {
    "db.sqlite3",
    "media.zip",
}


def safe_file_path(backup_id, filename):
    if filename not in ALLOWED_FILES:
        raise Http404("Недопустимый файл")

    root = Path(BACKUP_DIR).resolve()
    path = (root / backup_id / filename).resolve()

    if not str(path).startswith(str(root)):
        raise Http404("Недопустимый путь")

    return path


@login_required
@permission_required("core.view_backups", raise_exception=True)
def download_backup(request, backup_id, filename):
    path = safe_file_path(backup_id, filename)

    if not path.exists():
        raise Http404("Файл не найден")

    return FileResponse(
        path.open("rb"),
        as_attachment=True,
        filename=filename,
    )