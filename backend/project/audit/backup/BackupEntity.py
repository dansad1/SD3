from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.utils.timezone import make_aware

from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.project.audit.models.Backup import Backup


BACKUP_DIR = Path(settings.BASE_DIR) / "backups"
BACKUP_DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"


class BackupEntity(BaseEntity):
    model = Backup
    entity = "backup"

    list_display = [
        "id",
        "created_at",
        "name",
        "db_path",
        "media_path",
    ]

    def get_queryset(self, request):
        items = []

        if not BACKUP_DIR.exists():
            return items

        backup_root = BACKUP_DIR.resolve()

        for path in sorted(
            BACKUP_DIR.iterdir(),
            key=lambda item: item.name,
            reverse=True,
        ):
            try:
                resolved_path = path.resolve()
                resolved_path.relative_to(backup_root)
            except (OSError, ValueError):
                continue

            if not resolved_path.is_dir():
                continue

            created_at = self._parse_created(
                resolved_path.name,
            )

            if created_at is None:
                continue

            db_path = resolved_path / "db.sqlite3"
            media_path = resolved_path / "media.zip"

            obj = Backup(
                id=resolved_path.name,
                name=resolved_path.name,
                created_at=make_aware(created_at),
                db_path=(
                    f"{resolved_path.name}/db.sqlite3"
                    if db_path.is_file()
                    else ""
                ),
                media_path=(
                    f"{resolved_path.name}/media.zip"
                    if media_path.is_file()
                    else ""
                ),
            )

            obj.has_db = db_path.is_file()
            obj.has_media = media_path.is_file()

            items.append(obj)

        return items

    def _parse_created(self, folder_name):
        timestamp = folder_name[:19]

        try:
            return datetime.strptime(
                timestamp,
                BACKUP_DATE_FORMAT,
            )
        except ValueError:
            return None