from pathlib import Path
from shutil import rmtree

from django.apps import apps
from django.conf import settings
from django.core.management import (
    BaseCommand,
    CommandError,
    call_command,
)
from django.db import connections


class Command(BaseCommand):
    help = (
        "Полностью пересоздаёт локальную SQLite-базу "
        "с нуля или из последнего бэкапа"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Не запрашивать подтверждение",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Создать чистую базу",
        )
        parser.add_argument(
            "--restore-latest",
            action="store_true",
            help="Восстановить последний бэкап",
        )
        parser.add_argument(
            "--seed",
            action="store_true",
            help="Для чистой базы выполнить seed_all",
        )

    def handle(self, *args, **options):
        self._check_environment()
        self._check_options(options)

        restore_latest = self._select_reset_mode(
            clean=options["clean"],
            restore_latest=options["restore_latest"],
            skip_confirmation=options["yes"],
        )

        self._confirm_reset(
            restore_latest=restore_latest,
            skip_confirmation=options["yes"],
        )

        self._close_connections()
        self._remove_database()
        self._remove_project_migrations()
        self._remove_python_cache()

        app_labels = self._get_project_app_labels()

        if not app_labels:
            raise CommandError(
                "Локальные Django-приложения не найдены"
            )

        self.stdout.write("")
        self.stdout.write(
            "→ makemigrations"
        )

        call_command(
            "makemigrations",
            *app_labels,
            interactive=False,
        )

        if restore_latest:
            self.stdout.write("")
            self.stdout.write(
                "→ restore_backup --latest"
            )

            call_command(
                "restore_backup",
                latest=True,
                yes=True,
            )

        self.stdout.write("")
        self.stdout.write(
            "→ migrate"
        )

        call_command(
            "migrate",
            interactive=False,
        )

        self._check_required_tables()

        self.stdout.write("")
        self.stdout.write(
            "→ setup_system"
        )

        call_command(
            "setup_system",
        )

        if options["seed"]:
            self.stdout.write("")
            self.stdout.write(
                "→ seed_all"
            )

            call_command(
                "seed_all",
            )

        self.stdout.write("")

        if restore_latest:
            message = (
                "Система пересоздана из последнего бэкапа"
            )
        else:
            message = (
                "Создана чистая система"
            )

        self.stdout.write(
            self.style.SUCCESS(
                message
            )
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def _check_options(self, options):
        if (
            options["clean"]
            and options["restore_latest"]
        ):
            raise CommandError(
                "--clean нельзя использовать вместе "
                "с --restore-latest"
            )

        if (
            options["seed"]
            and options["restore_latest"]
        ):
            raise CommandError(
                "--seed нельзя использовать вместе "
                "с --restore-latest"
            )

        if (
            options["yes"]
            and not options["clean"]
            and not options["restore_latest"]
        ):
            raise CommandError(
                "При использовании --yes необходимо указать "
                "--clean или --restore-latest"
            )

    # =====================================================
    # ENVIRONMENT
    # =====================================================

    def _check_environment(self):
        if not settings.DEBUG:
            raise CommandError(
                "reset_system запрещён при DEBUG=False"
            )

        database = settings.DATABASES["default"]

        if (
            database["ENGINE"]
            != "django.db.backends.sqlite3"
        ):
            raise CommandError(
                "reset_system поддерживает только SQLite"
            )

        if not database.get("NAME"):
            raise CommandError(
                "Путь к SQLite-базе не указан"
            )

    # =====================================================
    # RESET MODE
    # =====================================================

    def _select_reset_mode(
        self,
        clean,
        restore_latest,
        skip_confirmation,
    ):
        if clean:
            return False

        if restore_latest:
            return True

        if skip_confirmation:
            raise CommandError(
                "Не выбран режим пересоздания системы"
            )

        self.stdout.write("")
        self.stdout.write(
            "Как пересоздать систему?"
        )
        self.stdout.write(
            "  1 — Чистая база"
        )
        self.stdout.write(
            "  2 — Восстановить последний бэкап"
        )

        while True:
            answer = input(
                "Выберите [1/2]: "
            ).strip().lower()

            if answer in {
                "1",
                "clean",
                "чистую",
                "чистая",
            }:
                return False

            if answer in {
                "2",
                "backup",
                "restore",
                "бэкап",
                "бэкапа",
            }:
                return True

            self.stderr.write(
                self.style.WARNING(
                    "Введите 1 для чистой базы "
                    "или 2 для восстановления бэкапа"
                )
            )

    def _confirm_reset(
        self,
        restore_latest,
        skip_confirmation,
    ):
        if skip_confirmation:
            return

        if restore_latest:
            mode = (
                "База и миграции проекта будут удалены, "
                "после чего будет восстановлен последний бэкап."
            )
        else:
            mode = (
                "База и миграции проекта будут удалены, "
                "после чего будет создана чистая система."
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                mode
            )
        )

        answer = input(
            "Продолжить? [yes/NO]: "
        )

        if answer.strip().lower() != "yes":
            raise CommandError(
                "Операция отменена"
            )

    # =====================================================
    # DATABASE
    # =====================================================

    def _close_connections(self):
        for connection in connections.all():
            connection.close()

    def _remove_database(self):
        database_name = settings.DATABASES[
            "default"
        ]["NAME"]

        database_path = Path(
            database_name
        )

        if not database_path.exists():
            self.stdout.write(
                "Файл базы отсутствует — удалять нечего"
            )
            return

        database_path.unlink()

        self.stdout.write(
            f"Удалена база: {database_path}"
        )

    # =====================================================
    # APPLICATIONS
    # =====================================================

    def _get_project_app_labels(self):
        labels = []

        for app_config in apps.get_app_configs():
            app_path = Path(
                app_config.path
            ).resolve()

            if not self._is_project_app(
                app_path
            ):
                continue

            labels.append(
                app_config.label
            )

        return sorted(
            set(labels)
        )

    def _is_project_app(
        self,
        app_path,
    ):
        base_dir = Path(
            settings.BASE_DIR
        ).resolve()

        try:
            app_path.relative_to(
                base_dir
            )
        except ValueError:
            return False

        return (
            ".venv"
            not in app_path.parts
        )

    # =====================================================
    # MIGRATIONS
    # =====================================================

    def _remove_project_migrations(self):
        for app_config in apps.get_app_configs():
            app_path = Path(
                app_config.path
            ).resolve()

            if not self._is_project_app(
                app_path
            ):
                continue

            migrations_path = (
                app_path / "migrations"
            )

            migrations_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            init_path = (
                migrations_path
                / "__init__.py"
            )

            init_path.touch(
                exist_ok=True
            )

            for path in migrations_path.iterdir():
                if path.name == "__init__.py":
                    continue

                if path.is_dir():
                    rmtree(
                        path,
                        ignore_errors=True,
                    )
                    continue

                if path.suffix in {
                    ".py",
                    ".pyc",
                }:
                    path.unlink()

            self.stdout.write(
                "Очищены миграции: "
                f"{app_config.label}"
            )

    # =====================================================
    # CACHE
    # =====================================================

    def _remove_python_cache(self):
        base_dir = Path(
            settings.BASE_DIR
        )

        for path in base_dir.rglob(
            "__pycache__"
        ):
            rmtree(
                path,
                ignore_errors=True,
            )

    # =====================================================
    # TABLE CHECK
    # =====================================================

    def _check_required_tables(self):
        connection = connections[
            "default"
        ]

        tables = set(
            connection
            .introspection
            .table_names()
        )

        required_tables = {
            "users_user",
            "users_permission",
        }

        missing_tables = (
            required_tables
            - tables
        )

        if not missing_tables:
            self.stdout.write(
                self.style.SUCCESS(
                    "Критичные таблицы созданы"
                )
            )
            return

        missing = ", ".join(
            sorted(missing_tables)
        )

        raise CommandError(
            "После migrate отсутствуют "
            f"таблицы: {missing}"
        )