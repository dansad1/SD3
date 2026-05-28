import os
from datetime import datetime

from django.conf import settings
from django.utils.timezone import make_aware


from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.project.audit.models.Backup import Backup

BACKUP_DIR = os.path.join(settings.BASE_DIR, "backups")


class BackupEntity(BaseEntity):
    model = Backup
    entity = "backup"

    list_display = [
        "id",
        "created",
        "name",
        "db_path",
        "media_path",
    ]

    def get_queryset(self, request):
        items = []

        if not os.path.exists(BACKUP_DIR):
            return items

        folders = sorted(os.listdir(BACKUP_DIR), reverse=True)

        for folder in folders:
            path = os.path.abspath(
                os.path.join(BACKUP_DIR, folder)
            )

            backup_root = os.path.abspath(BACKUP_DIR)

            if not path.startswith(backup_root):
                continue

            if not os.path.isdir(path):
                continue

            try:
                created = datetime.strptime(
                    folder.split("_")[0] + "_" + folder.split("_")[1],
                    "%Y-%m-%d_%H-%M-%S",
                )
            except Exception:
                continue

            db_path = os.path.join(path, "db.sqlite3")
            media_path = os.path.join(path, "media.zip")

            obj = Backup(
                id=folder,
                name=folder,
                created=make_aware(created),
                db_path=f"{folder}/db.sqlite3",
                media_path=f"{folder}/media.zip",
            )

            obj.has_db = os.path.exists(db_path)
            obj.has_media = os.path.exists(media_path)

            items.append(obj)

        return items