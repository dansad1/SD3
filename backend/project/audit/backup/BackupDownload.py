from core.api.engine.action.Base.BaseAction import BaseAction


def get_backup_id(payload, ctx):
    return (
        payload.get("id")
        or payload.get("backup_id")
        or (ctx or {}).get("id")
    )


class DownloadDatabaseBackupAction(BaseAction):
    code = "backup.download.db"
    permission = "view_backups"

    def run(self, request, payload, ctx):
        backup_id = get_backup_id(payload, ctx)

        if not backup_id:
            return {
                "status": "error",
                "errors": {
                    "__all__": ["Не указан backup id"]
                },
            }

        return {
            "status": "ok",
            "download": f"/api/backup/{backup_id}/download/db.sqlite3",
        }


class DownloadMediaBackupAction(BaseAction):
    code = "backup.download.media"
    permission = "view_backups"

    def run(self, request, payload, ctx):
        backup_id = get_backup_id(payload, ctx)

        if not backup_id:
            return {
                "status": "error",
                "errors": {
                    "__all__": ["Не указан backup id"]
                },
            }

        return {
            "status": "ok",
            "download": f"/api/backup/{backup_id}/download/media.zip",
        }