import sys
import subprocess

from backend.engine.action.Base.BaseAction import BaseAction


class BackupCreateAction(BaseAction):
    code = "backup.create"
    permission = "view_backups"

    def run(self, request, payload, ctx):
        try:
            subprocess.run(
                [
                    sys.executable,
                    "manage.py",
                    "backup_data",
                ],
                check=True,
                timeout=300,
            )

            return {
                "status": "ok",
                "message": "Бэкап успешно создан",
                "effects": [
                    {
                        "type": "reload",
                    }
                ],
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "errors": {
                    "__all__": [
                        "Создание бэкапа превысило лимит времени"
                    ]
                },
            }

        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "errors": {
                    "__all__": [
                        f"Ошибка создания бэкапа: {e}"
                    ]
                },
            }