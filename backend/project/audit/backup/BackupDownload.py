from urllib.parse import quote

from backend.engine.action.Base.BaseAction import BaseAction


def get_backup_id(payload, ctx):
    payload = payload or {}
    ctx = ctx or {}

    backup_id = (
        payload.get("id")
        or payload.get("backup_id")
        or ctx.get("id")
    )

    if backup_id is None:
        return None

    backup_id = str(backup_id).strip()

    if not backup_id:
        return None

    return backup_id


def build_download_url(backup_id, filename):
    safe_backup_id = quote(
        backup_id,
        safe="",
    )

    return (
        f"/api/backup/"
        f"{safe_backup_id}/download/"
        f"{filename}"
    )


class DownloadDatabaseBackupAction(BaseAction):
    code = "backup.download.db"
    permission = "view_backups"

    def run(self, request, payload, ctx):
        backup_id = get_backup_id(
            payload,
            ctx,
        )

        if not backup_id:
            return {
                "status": "error",
                "errors": {
                    "__all__": [
                        "Не указан backup id",
                    ],
                },
            }

        return {
            "status": "ok",
            "download": build_download_url(
                backup_id,
                "db.sqlite3",
            ),
        }


class DownloadMediaBackupAction(BaseAction):
    code = "backup.download.media"
    permission = "view_backups"

    def run(self, request, payload, ctx):
        backup_id = get_backup_id(
            payload,
            ctx,
        )

        if not backup_id:
            return {
                "status": "error",
                "errors": {
                    "__all__": [
                        "Не указан backup id",
                    ],
                },
            }

        return {
            "status": "ok",
            "download": build_download_url(
                backup_id,
                "media.zip",
            ),
        }