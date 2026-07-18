import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Создаёт резервную копию SQLite и media"

    def handle(self, *args, **options):
        self._validate_database()

        backup_root = Path(settings.BASE_DIR) / "backups"
        backup_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_name = timezone.localtime().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        backup_path = backup_root / backup_name
        temporary_path = backup_root / f".{backup_name}.tmp"

        if temporary_path.exists():
            shutil.rmtree(temporary_path)

        temporary_path.mkdir(
            parents=True,
            exist_ok=False,
        )

        try:
            database_path = temporary_path / "db.sqlite3"
            media_path = temporary_path / "media.zip"

            self.stdout.write("→ Резервная копия базы")
            self._backup_database(database_path)

            self.stdout.write("→ Резервная копия media")
            self._backup_media(media_path)

            if backup_path.exists():
                raise CommandError(
                    f"Каталог бэкапа уже существует: {backup_path}"
                )

            temporary_path.rename(backup_path)

        except Exception:
            shutil.rmtree(
                temporary_path,
                ignore_errors=True,
            )
            raise

        self.stdout.write(
            self.style.SUCCESS(
                f"Бэкап успешно создан: {backup_path}"
            )
        )

    def _validate_database(self):
        database = settings.DATABASES["default"]

        if database["ENGINE"] != "django.db.backends.sqlite3":
            raise CommandError(
                "Команда поддерживает только SQLite"
            )

        database_name = database.get("NAME")

        if not database_name:
            raise CommandError(
                "Путь к SQLite не указан"
            )

        database_path = Path(database_name)

        if not database_path.exists():
            raise CommandError(
                f"Файл базы не найден: {database_path}"
            )

    def _backup_database(self, destination):
        database_path = Path(
            settings.DATABASES["default"]["NAME"]
        )

        source_connection = None
        destination_connection = None

        try:
            source_connection = sqlite3.connect(
                database_path,
                timeout=30,
            )
            destination_connection = sqlite3.connect(
                destination,
                timeout=30,
            )

            source_connection.backup(
                destination_connection,
            )

        finally:
            if destination_connection is not None:
                destination_connection.close()

            if source_connection is not None:
                source_connection.close()

    def _backup_media(self, destination):
        media_root = Path(settings.MEDIA_ROOT)

        if not media_root.exists():
            media_root.mkdir(
                parents=True,
                exist_ok=True,
            )

        archive_base = destination.with_suffix("")

        created_archive = shutil.make_archive(
            base_name=str(archive_base),
            format="zip",
            root_dir=str(media_root),
        )

        created_path = Path(created_archive)

        if created_path != destination:
            created_path.replace(destination)