import os
import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.utils import timezone


class Command(BaseCommand):

    help = (
        "Создаёт резервную копию PostgreSQL "
        "и каталога media"
    )

    DATABASE_BACKUP_NAME = "database.dump"
    MEDIA_BACKUP_NAME = "media.zip"

    DEFAULT_KEEP = 5

    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--keep",
            type=int,
            default=self.DEFAULT_KEEP,
            help=(
                "Количество последних резервных "
                "копий, которые нужно сохранить"
            ),
        )

    def handle(
        self,
        *args,
        **options,
    ):
        keep = options["keep"]

        if keep < 1:
            raise CommandError(
                "--keep должен быть больше нуля"
            )

        self._validate_database()

        backup_root = (
            Path(settings.BASE_DIR)
            / "backups"
        )

        backup_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_name = (
            timezone.localtime()
            .strftime(
                "%Y-%m-%d_%H-%M-%S",
            )
        )

        backup_path = (
            backup_root
            / backup_name
        )

        temporary_path = (
            backup_root
            / f".{backup_name}.tmp"
        )

        if temporary_path.exists():
            shutil.rmtree(
                temporary_path,
                ignore_errors=True,
            )

        temporary_path.mkdir(
            parents=True,
            exist_ok=False,
        )

        try:
            database_path = (
                temporary_path
                / self.DATABASE_BACKUP_NAME
            )

            media_path = (
                temporary_path
                / self.MEDIA_BACKUP_NAME
            )

            self.stdout.write(
                "→ Резервная копия PostgreSQL"
            )

            self._backup_database(
                database_path,
            )

            self.stdout.write(
                "→ Резервная копия media"
            )

            self._backup_media(
                media_path,
            )

            if backup_path.exists():
                raise CommandError(
                    (
                        "Каталог резервной копии "
                        "уже существует: "
                        f"{backup_path}"
                    )
                )

            temporary_path.rename(
                backup_path,
            )

        except Exception:
            shutil.rmtree(
                temporary_path,
                ignore_errors=True,
            )

            raise

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Бэкап успешно создан: "
                    f"{backup_path}"
                )
            )
        )

        self._cleanup_old_backups(
            backup_root=backup_root,
            keep=keep,
        )

    # =====================================================
    # DATABASE VALIDATION
    # =====================================================

    def _validate_database(
        self,
    ):
        database = (
            settings.DATABASES[
                "default"
            ]
        )

        engine = database.get(
            "ENGINE",
            "",
        )

        if engine not in {
            "django.db.backends.postgresql",
            (
                "django.db.backends."
                "postgresql_psycopg2"
            ),
        }:
            raise CommandError(
                (
                    "Команда поддерживает "
                    "только PostgreSQL"
                )
            )

        if not database.get("NAME"):
            raise CommandError(
                "Имя базы данных не указано"
            )

        if not database.get("USER"):
            raise CommandError(
                "Пользователь PostgreSQL не указан"
            )

        if shutil.which("pg_dump") is None:
            raise CommandError(
                (
                    "Команда pg_dump не найдена. "
                    "Установите postgresql-client."
                )
            )

    # =====================================================
    # DATABASE BACKUP
    # =====================================================

    def _backup_database(
        self,
        destination,
    ):
        database = (
            settings.DATABASES[
                "default"
            ]
        )

        name = str(
            database.get(
                "NAME",
                "",
            )
        )

        user = str(
            database.get(
                "USER",
                "",
            )
        )

        password = str(
            database.get(
                "PASSWORD",
                "",
            )
        )

        host = str(
            database.get(
                "HOST",
                "",
            )
            or "localhost"
        )

        port = str(
            database.get(
                "PORT",
                "",
            )
            or "5432"
        )

        environment = os.environ.copy()

        if password:
            environment[
                "PGPASSWORD"
            ] = password

        command = [
            "pg_dump",

            "--host",
            host,

            "--port",
            port,

            "--username",
            user,

            "--format",
            "custom",

            "--compress",
            "6",

            "--no-password",

            "--file",
            str(destination),

            name,
        ]

        try:
            result = subprocess.run(
                command,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

        except OSError as exc:
            raise CommandError(
                (
                    "Не удалось запустить "
                    "pg_dump"
                )
            ) from exc

        if result.returncode != 0:
            destination.unlink(
                missing_ok=True,
            )

            error = (
                result.stderr.strip()
                or "Неизвестная ошибка pg_dump"
            )

            raise CommandError(
                (
                    "Не удалось создать "
                    "резервную копию PostgreSQL: "
                    f"{error}"
                )
            )

        if (
            not destination.exists()
            or destination.stat().st_size == 0
        ):
            destination.unlink(
                missing_ok=True,
            )

            raise CommandError(
                (
                    "pg_dump завершился без ошибки, "
                    "но файл резервной копии пуст"
                )
            )

    # =====================================================
    # MEDIA BACKUP
    # =====================================================

    def _backup_media(
        self,
        destination,
    ):
        media_root = Path(
            settings.MEDIA_ROOT,
        )

        media_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        archive_base = (
            destination
            .with_suffix("")
        )

        created_archive = (
            shutil.make_archive(
                base_name=str(
                    archive_base,
                ),
                format="zip",
                root_dir=str(
                    media_root,
                ),
            )
        )

        created_path = Path(
            created_archive,
        )

        if created_path != destination:
            created_path.replace(
                destination,
            )

        if not destination.exists():
            raise CommandError(
                (
                    "Не удалось создать "
                    "архив media"
                )
            )

    # =====================================================
    # RETENTION
    # =====================================================

    def _cleanup_old_backups(
        self,
        backup_root,
        keep,
    ):
        backups = sorted(
            [
                path
                for path
                in backup_root.iterdir()
                if (
                    path.is_dir()
                    and not path.name.startswith(
                        ".",
                    )
                )
            ],
            key=lambda path: (
                path.stat().st_mtime
            ),
            reverse=True,
        )

        old_backups = backups[
            keep:
        ]

        for path in old_backups:
            shutil.rmtree(
                path,
                ignore_errors=True,
            )

            self.stdout.write(
                f"   🗑 удалён старый бэкап: "
                f"{path.name}"
            )