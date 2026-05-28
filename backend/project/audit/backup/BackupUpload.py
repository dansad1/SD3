import os
import uuid
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

from django.conf import settings

from backend.engine.action.Base.BaseAction import BaseAction

BACKUP_DIR = os.path.join(settings.BASE_DIR, "backups")


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


class BackupUploadAction(BaseAction):
    code = "backup.upload"
    permission = "view_backups"

    def run(self, request, payload, ctx):
        file = request.FILES.get("file")

        if not file:
            return {
                "status": "error",
                "errors": {
                    "__all__": ["Файл не выбран"]
                },
            }

        folder_name = (
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            + "_"
            + uuid.uuid4().hex[:6]
        )

        backup_folder = Path(BACKUP_DIR) / folder_name
        backup_folder.mkdir(parents=True, exist_ok=False)

        uploaded_zip_path = backup_folder / "uploaded.zip"

        try:
            with open(uploaded_zip_path, "wb+") as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            safe_extract_zip(
                uploaded_zip_path,
                backup_folder,
            )

            uploaded_zip_path.unlink(missing_ok=True)

            db_path = backup_folder / "db.sqlite3"
            media_path = backup_folder / "media.zip"

            if not db_path.exists():
                raise ValueError("В архиве нет db.sqlite3")

            if not media_path.exists():
                raise ValueError("В архиве нет media.zip")

            return {
                "status": "ok",
                "message": f"Бэкап {folder_name} успешно загружен",
                "effects": [
                    {
                        "type": "reload",
                    }
                ],
            }

        except zipfile.BadZipFile:
            shutil.rmtree(backup_folder, ignore_errors=True)

            return {
                "status": "error",
                "errors": {
                    "__all__": [
                        "Файл не является корректным ZIP архивом"
                    ]
                },
            }

        except Exception as e:
            shutil.rmtree(backup_folder, ignore_errors=True)

            return {
                "status": "error",
                "errors": {
                    "__all__": [str(e)]
                },
            }