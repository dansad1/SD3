import shutil
import sqlite3
import zipfile
from pathlib import Path
from shutil import rmtree

from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.db import connections


BACKUP_DIR = Path(settings.BASE_DIR) / "backups"

DATABASE_BACKUP_NAME = "db.sqlite3"
MEDIA_BACKUP_NAME = "media.zip"

MAX_MEDIA_FILES = 100_000
MAX_MEDIA_SIZE = 10 * 1024 * 1024 * 1024


class Command(BaseCommand):
    help = "Восстанавливает SQLite и media из резервной копии"

    def add_arguments(self, parser):
        parser.add_argument(
            "backup_id",
            nargs="?",
            help="Имя каталога бэкапа",
        )
        parser.add_argument(
            "--latest",
            action="store_true",
            help="Использовать последний корректный бэкап",
        )
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Не запрашивать подтверждение",
        )
        parser.add_argument(
            "--database-only",
            action="store_true",
            help="Восстановить только базу данных",
        )
        parser.add_argument(
            "--media-only",
            action="store_true",
            help="Восстановить только media",
        )

    def handle(self, *args, **options):
        self._check_environment()
        self._check_options(options)

        backup_path = self._resolve_backup(
            backup_id=options["backup_id"],
            latest=options["latest"],
        )

        restore_database = not options["media_only"]
        restore_media = not options["database_only"]

        self._validate_backup(
            backup_path=backup_path,
            require_database=restore_database,
            require_media=restore_media,
        )

        self._confirm(
            backup_path=backup_path,
            restore_database=restore_database,
            restore_media=restore_media,
            skip_confirmation=options["yes"],
        )

        if restore_database:
            self.stdout.write(
                f"→ restore database: {backup_path.name}"
            )
            self._restore_database(
                backup_path
            )

        if restore_media:
            self.stdout.write(
                f"→ restore media: {backup_path.name}"
            )
            self._restore_media(
                backup_path
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Бэкап {backup_path.name} успешно восстановлен"
            )
        )

    def _check_environment(self):
        database = settings.DATABASES["default"]

        if (
            database["ENGINE"]
            != "django.db.backends.sqlite3"
        ):
            raise CommandError(
                "restore_backup поддерживает только SQLite"
            )

        database_name = database.get("NAME")

        if not database_name:
            raise CommandError(
                "Путь к SQLite-базе не указан"
            )

    def _check_options(self, options):
        if (
            options["backup_id"]
            and options["latest"]
        ):
            raise CommandError(
                "Укажите либо backup_id, либо --latest"
            )

        if (
            not options["backup_id"]
            and not options["latest"]
        ):
            raise CommandError(
                "Укажите backup_id или используйте --latest"
            )

        if (
            options["database_only"]
            and options["media_only"]
        ):
            raise CommandError(
                "--database-only нельзя использовать "
                "вместе с --media-only"
            )

    def _resolve_backup(
        self,
        backup_id,
        latest,
    ):
        if latest:
            backup_path = self._find_latest_backup()

            if backup_path is None:
                raise CommandError(
                    "Корректный бэкап не найден"
                )

            return backup_path

        return self._get_backup_path(
            backup_id
        )

    def _get_backup_path(
        self,
        backup_id,
    ):
        backup_root = BACKUP_DIR.resolve()

        backup_path = (
            backup_root / str(backup_id)
        ).resolve()

        try:
            backup_path.relative_to(
                backup_root
            )
        except ValueError as exc:
            raise CommandError(
                "Недопустимый путь резервной копии"
            ) from exc

        if not backup_path.is_dir():
            raise CommandError(
                f"Бэкап не найден: {backup_id}"
            )

        return backup_path

    def _find_latest_backup(self):
        if not BACKUP_DIR.exists():
            return None

        backups = []

        for path in BACKUP_DIR.iterdir():
            if not path.is_dir():
                continue

            if path.name.startswith("."):
                continue

            database_path = (
                path / DATABASE_BACKUP_NAME
            )

            if not database_path.is_file():
                continue

            backups.append(path)

        if not backups:
            return None

        return max(
            backups,
            key=lambda path: path.stat().st_mtime,
        )

    def _validate_backup(
        self,
        backup_path,
        require_database,
        require_media,
    ):
        database_path = (
            backup_path / DATABASE_BACKUP_NAME
        )

        media_path = (
            backup_path / MEDIA_BACKUP_NAME
        )

        if require_database:
            if not database_path.is_file():
                raise CommandError(
                    "В бэкапе отсутствует db.sqlite3"
                )

            self._validate_sqlite_database(
                database_path
            )

        if require_media:
            if not media_path.is_file():
                raise CommandError(
                    "В бэкапе отсутствует media.zip"
                )

            self._validate_media_archive(
                media_path
            )

    def _validate_sqlite_database(
        self,
        database_path,
    ):
        connection = None

        try:
            connection = sqlite3.connect(
                (
                    f"file:{database_path.resolve()}"
                    "?mode=ro"
                ),
                uri=True,
            )

            result = connection.execute(
                "PRAGMA integrity_check"
            ).fetchone()

        except sqlite3.Error as exc:
            raise CommandError(
                "db.sqlite3 не является корректной SQLite-базой"
            ) from exc

        finally:
            if connection is not None:
                connection.close()

        if (
            not result
            or result[0] != "ok"
        ):
            raise CommandError(
                "SQLite-база в бэкапе повреждена"
            )

    def _validate_media_archive(
        self,
        archive_path,
    ):
        try:
            with zipfile.ZipFile(
                archive_path,
                "r",
            ) as archive:
                bad_file = archive.testzip()

                if bad_file:
                    raise CommandError(
                        f"В media.zip повреждён файл: {bad_file}"
                    )

        except zipfile.BadZipFile as exc:
            raise CommandError(
                "media.zip повреждён"
            ) from exc

    def _confirm(
        self,
        backup_path,
        restore_database,
        restore_media,
        skip_confirmation,
    ):
        if skip_confirmation:
            return

        targets = []

        if restore_database:
            targets.append("база данных")

        if restore_media:
            targets.append("media")

        target_text = " и ".join(
            targets
        )

        answer = input(
            f"Будут заменены {target_text} из бэкапа "
            f"{backup_path.name}. Продолжить? [yes/NO]: "
        )

        if answer.strip().lower() != "yes":
            raise CommandError(
                "Операция отменена"
            )

    def _close_connections(self):
        for connection in connections.all():
            connection.close()

    def _restore_database(
        self,
        backup_path,
    ):
        source = (
            backup_path / DATABASE_BACKUP_NAME
        )

        target = Path(
            settings.DATABASES["default"]["NAME"]
        ).resolve()

        temporary_target = (
            target.parent / f".{target.name}.restore"
        )

        old_target = (
            target.parent / f".{target.name}.before_restore"
        )

        self._close_connections()

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_target.unlink(
            missing_ok=True
        )

        old_target.unlink(
            missing_ok=True
        )

        try:
            shutil.copy2(
                source,
                temporary_target,
            )

            self._validate_sqlite_database(
                temporary_target
            )

            if target.exists():
                target.replace(
                    old_target
                )

            temporary_target.replace(
                target
            )

            old_target.unlink(
                missing_ok=True
            )

        except Exception:
            temporary_target.unlink(
                missing_ok=True
            )

            if old_target.exists():
                if target.exists():
                    target.unlink()

                old_target.replace(
                    target
                )

            raise

    def _restore_media(
        self,
        backup_path,
    ):
        archive_path = (
            backup_path / MEDIA_BACKUP_NAME
        )

        media_target = Path(
            settings.MEDIA_ROOT
        ).resolve()

        temporary_media = (
            media_target.parent
            / f".{media_target.name}.restore"
        )

        old_media = (
            media_target.parent
            / f".{media_target.name}.before_restore"
        )

        rmtree(
            temporary_media,
            ignore_errors=True,
        )

        rmtree(
            old_media,
            ignore_errors=True,
        )

        temporary_media.mkdir(
            parents=True,
            exist_ok=False,
        )

        try:
            self._safe_extract_zip(
                archive_path=archive_path,
                target_dir=temporary_media,
            )

            if media_target.exists():
                media_target.replace(
                    old_media
                )

            temporary_media.replace(
                media_target
            )

            rmtree(
                old_media,
                ignore_errors=True,
            )

        except Exception:
            rmtree(
                temporary_media,
                ignore_errors=True,
            )

            if old_media.exists():
                if media_target.exists():
                    rmtree(
                        media_target,
                        ignore_errors=True,
                    )

                old_media.replace(
                    media_target
                )

            raise

    def _safe_extract_zip(
        self,
        archive_path,
        target_dir,
    ):
        target_dir = Path(
            target_dir
        ).resolve()

        total_size = 0
        file_count = 0

        with zipfile.ZipFile(
            archive_path,
            "r",
        ) as archive:
            members = archive.infolist()

            for member in members:
                destination = (
                    target_dir / member.filename
                ).resolve()

                try:
                    destination.relative_to(
                        target_dir
                    )
                except ValueError as exc:
                    raise CommandError(
                        "media.zip содержит небезопасный путь"
                    ) from exc

                unix_mode = (
                    member.external_attr >> 16
                )

                if (
                    unix_mode & 0o170000
                ) == 0o120000:
                    raise CommandError(
                        "media.zip содержит символическую ссылку"
                    )

                if member.is_dir():
                    continue

                file_count += 1
                total_size += member.file_size

                if file_count > MAX_MEDIA_FILES:
                    raise CommandError(
                        "media.zip содержит слишком много файлов"
                    )

                if total_size > MAX_MEDIA_SIZE:
                    raise CommandError(
                        "Распакованный media.zip слишком большой"
                    )

            for member in members:
                destination = (
                    target_dir / member.filename
                ).resolve()

                if member.is_dir():
                    destination.mkdir(
                        parents=True,
                        exist_ok=True,
                    )
                    continue

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                with archive.open(
                    member,
                    "r",
                ) as source:
                    with destination.open(
                        "wb",
                    ) as target:
                        shutil.copyfileobj(
                            source,
                            target,
                            length=1024 * 1024,
                        )