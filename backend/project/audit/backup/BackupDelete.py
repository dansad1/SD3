import re
import shutil
from pathlib import Path

from django.conf import settings

from backend.engine.action.Base.BaseAction import BaseAction


BACKUP_DIR = Path(settings.BASE_DIR) / "backups"

BACKUP_ID_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}_"
    r"\d{2}-\d{2}-\d{2}"
    r"(?:_[0-9a-f]{6})?$"
)


def error_response(message):
    return {
        "status": "error",
        "errors": {
            "__all__": [
                message,
            ],
        },
    }


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


def get_backup_path(backup_id):
    if not BACKUP_ID_PATTERN.fullmatch(backup_id):
        raise ValueError(
            "Некорректный идентификатор резервной копии"
        )

    backup_root = BACKUP_DIR.resolve()
    backup_path = (
        backup_root / backup_id
    ).resolve()

    try:
        backup_path.relative_to(backup_root)
    except ValueError as exc:
        raise ValueError(
            "Недопустимый путь резервной копии"
        ) from exc

    return backup_path


class BackupDeleteAction(BaseAction):
    code = "backup.delete"
    permission = "delete_backups"
    confirm = "Удалить резервную копию?"

    def run(self, request, payload, ctx=None):
        backup_id = get_backup_id(
            payload,
            ctx,
        )

        if not backup_id:
            return error_response(
                "Не указан backup id"
            )

        try:
            backup_path = get_backup_path(
                backup_id
            )

            if not backup_path.exists():
                return error_response(
                    "Резервная копия не найдена"
                )

            if not backup_path.is_dir():
                return error_response(
                    "Объект резервной копии не является каталогом"
                )

            shutil.rmtree(
                backup_path
            )

            return {
                "status": "ok",
                "message": (
                    f"Бэкап {backup_id} удалён"
                ),
                "effects": [
                    {
                        "type": "table.reload",
                        "entity": "backup",
                    },
                    {
                        "type": "toast",
                        "variant": "success",
                        "message": "Резервная копия удалена",
                    },
                ],
            }

        except ValueError as exc:
            return error_response(
                str(exc)
            )

        except OSError:
            return error_response(
                "Не удалось удалить резервную копию"
            )