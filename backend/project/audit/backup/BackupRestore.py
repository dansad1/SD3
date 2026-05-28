import os
import shutil
import zipfile
from pathlib import Path

from django.conf import settings

from backend.engine.action.Base.BaseAction import BaseAction

BACKUP_DIR = os.path.join(settings.BASE_DIR, "backups")


def safe_backup_path(backup_id):
    root = Path(BACKUP_DIR).resolve()
    path = (root / backup_id).resolve()

    if not str(path).startswith(str(root)):
        raise ValueError("Недопустимый backup path")

    return path


def safe_extract_zip(zip_path, target_dir):
    target_dir = Path(target_dir).resolve()

    with zipfile.ZipFile(zip_path, "r") as zipf:
        for member in zipf.infolist():
            member_path = (target_dir / member.filename).resolve()

            if not str(member_path).startswith(str(target_dir)):
                raise ValueError(
                    "ZIP содержит небезопасный путь"
                )

        zipf.extractall(target_dir)


class BackupRestoreAction(BaseAction):
    code = "backup.restore"
    permission = "view_backups"
    confirm = "Восстановить систему из этого бэкапа?"

    def run(self, request, payload, ctx=None):
        backup_id = (
            payload.get("id")
            or payload.get("backup_id")
            or (ctx or {}).get("id")
        )

        if not backup_id:
            return {
                "status": "error",
                "errors": {
                    "__all__": ["Не указан backup id"]
                },
            }

        try:
            backup_path = safe_backup_path(backup_id)

            db_path = backup_path / "db.sqlite3"
            media_zip_path = backup_path / "media.zip"

            if not db_path.exists():
                return {
                    "status": "error",
                    "errors": {
                        "__all__": ["Файл db.sqlite3 не найден"]
                    },
                }

            if not media_zip_path.exists():
                return {
                    "status": "error",
                    "errors": {
                        "__all__": ["Файл media.zip не найден"]
                    },
                }

            db_target = Path(settings.DATABASES["default"]["NAME"])
            db_tmp = db_target.with_suffix(".restore_tmp")

            shutil.copy2(db_path, db_tmp)
            shutil.move(str(db_tmp), str(db_target))

            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            safe_extract_zip(
                media_zip_path,
                settings.MEDIA_ROOT,
            )

            return {
                "status": "ok",
                "message": f"Бэкап {backup_id} успешно восстановлен",
                "effects": [
                    {
                        "type": "reload",
                    }
                ],
            }

        except Exception as e:
            return {
                "status": "error",
                "errors": {
                    "__all__": [str(e)]
                },
            }