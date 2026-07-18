import shutil
import tempfile
import zipfile
from pathlib import Path

from django.conf import settings
from django.db import connections

from backend.engine.action.Base.BaseAction import BaseAction


BACKUP_DIR = Path(settings.BASE_DIR) / "backups"


def safe_backup_path(backup_id):
    root = BACKUP_DIR.resolve()
    path = (root / str(backup_id)).resolve()

    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            "Недопустимый путь резервной копии"
        ) from exc

    return path


def safe_extract_zip(zip_path, target_dir):
    target_dir = Path(target_dir).resolve()
    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    with zipfile.ZipFile(zip_path, "r") as archive:
        for member in archive.infolist():
            member_path = (
                target_dir / member.filename
            ).resolve()

            try:
                member_path.relative_to(target_dir)
            except ValueError as exc:
                raise ValueError(
                    "ZIP содержит небезопасный путь"
                ) from exc

            if member.is_dir():
                continue

            if member.external_attr >> 16 & 0o120000:
                raise ValueError(
                    "ZIP содержит символическую ссылку"
                )

        archive.extractall(target_dir)


class BackupRestoreAction(BaseAction):
    code = "backup.restore"
    permission = "restore_backups"
    confirm = "Восстановить систему из этого бэкапа?"

    def run(self, request, payload, ctx=None):
        backup_id = (
            payload.get("id")
            or payload.get("backup_id")
            or (ctx or {}).get("id")
        )

        if not backup_id:
            return self._error(
                "Не указан backup id"
            )

        try:
            backup_path = safe_backup_path(
                backup_id
            )

            db_source = backup_path / "db.sqlite3"
            media_source = backup_path / "media.zip"

            if not db_source.is_file():
                return self._error(
                    "Файл db.sqlite3 не найден"
                )

            if not media_source.is_file():
                return self._error(
                    "Файл media.zip не найден"
                )

            self._restore(
                db_source=db_source,
                media_source=media_source,
            )

            return {
                "status": "ok",
                "message": (
                    f"Бэкап {backup_id} успешно восстановлен"
                ),
                "effects": [
                    {
                        "type": "reload",
                    },
                ],
            }

        except (
            ValueError,
            OSError,
            zipfile.BadZipFile,
        ):
            return self._error(
                "Не удалось восстановить резервную копию"
            )

    def _restore(
        self,
        db_source,
        media_source,
    ):
        db_target = Path(
            settings.DATABASES["default"]["NAME"]
        ).resolve()

        media_target = Path(
            settings.MEDIA_ROOT
        ).resolve()

        restore_root = Path(
            tempfile.mkdtemp(
                prefix="restore_",
                dir=settings.BASE_DIR,
            )
        )

        db_staged = restore_root / "db.sqlite3"
        media_staged = restore_root / "media"

        db_old = db_target.with_suffix(
            ".before_restore"
        )

        media_old = media_target.with_name(
            f"{media_target.name}.before_restore"
        )

        try:
            shutil.copy2(
                db_source,
                db_staged,
            )

            safe_extract_zip(
                media_source,
                media_staged,
            )

            for connection in connections.all():
                connection.close()

            if db_old.exists():
                db_old.unlink()

            if media_old.exists():
                shutil.rmtree(
                    media_old,
                    ignore_errors=True,
                )

            if db_target.exists():
                shutil.move(
                    db_target,
                    db_old,
                )

            if media_target.exists():
                shutil.move(
                    media_target,
                    media_old,
                )

            shutil.move(
                db_staged,
                db_target,
            )

            shutil.move(
                media_staged,
                media_target,
            )

            if db_old.exists():
                db_old.unlink()

            if media_old.exists():
                shutil.rmtree(
                    media_old,
                    ignore_errors=True,
                )

        except Exception:
            self._rollback(
                db_target=db_target,
                db_old=db_old,
                media_target=media_target,
                media_old=media_old,
            )
            raise

        finally:
            shutil.rmtree(
                restore_root,
                ignore_errors=True,
            )

    def _rollback(
        self,
        db_target,
        db_old,
        media_target,
        media_old,
    ):
        for connection in connections.all():
            connection.close()

        if db_old.exists():
            if db_target.exists():
                db_target.unlink()

            shutil.move(
                db_old,
                db_target,
            )

        if media_old.exists():
            if media_target.exists():
                shutil.rmtree(
                    media_target,
                    ignore_errors=True,
                )

            shutil.move(
                media_old,
                media_target,
            )

    def _error(self, message):
        return {
            "status": "error",
            "errors": {
                "__all__": [
                    message,
                ],
            },
        }