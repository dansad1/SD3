from django.core.management import call_command

from backend.engine.action.Base.BaseAction import BaseAction


class BackupCreateAction(BaseAction):
    code = "backup.create"
    permission = "view_backups"

    def run(self, request, payload, ctx):
        call_command(
            "backup_data",
            verbosity=1,
        )

        return {
            "status": "ok",
            "message": "Бэкап успешно создан",
            "effects": [
                {
                    "type": "reload",
                },
            ],
        }