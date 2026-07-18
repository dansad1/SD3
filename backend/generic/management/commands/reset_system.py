from pathlib import Path
from shutil import rmtree

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import connections


class Command(BaseCommand):
    help = "Полностью пересоздаёт локальную SQLite-базу"

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Не запрашивать подтверждение",
        )
        parser.add_argument(
            "--seed",
            action="store_true",
            help="После настройки выполнить seed_all",
        )

    def handle(self, *args, **options):
        self._check_environment()
        self._confirm(options["yes"])

        self._close_connections()
        self._remove_database()
        self._remove_project_migrations()
        self._remove_python_cache()

        self.stdout.write("→ makemigrations")
        call_command(
            "makemigrations",
            *self._get_project_app_labels(),
            interactive=False,
        )

        self.stdout.write("→ migrate")
        call_command(
            "migrate",
            interactive=False,
        )

        self._check_required_tables()

        self.stdout.write("→ setup_system")
        call_command("setup_system")

        if options["seed"]:
            self.stdout.write("→ seed_all")
            call_command("seed_all")

        self.stdout.write(
            self.style.SUCCESS(
                "База успешно пересоздана"
            )
        )

    def _check_environment(self):
        if not settings.DEBUG:
            raise RuntimeError(
                "reset_system запрещён при DEBUG=False"
            )

        database = settings.DATABASES["default"]

        if database["ENGINE"] != "django.db.backends.sqlite3":
            raise RuntimeError(
                "reset_system сейчас поддерживает только SQLite"
            )

    def _confirm(self, skip_confirmation):
        if skip_confirmation:
            return

        answer = input(
            "Будет удалена база и миграции проекта. "
            "Продолжить? [yes/NO]: "
        )

        if answer.strip().lower() != "yes":
            raise RuntimeError("Операция отменена")

    def _close_connections(self):
        for connection in connections.all():
            connection.close()

    def _remove_database(self):
        database_name = settings.DATABASES["default"]["NAME"]
        database_path = Path(database_name)

        if database_path.exists():
            database_path.unlink()

            self.stdout.write(
                f"Удалена база: {database_path}"
            )

    def _get_project_app_labels(self):
        labels = []

        for app_config in apps.get_app_configs():
            app_path = Path(app_config.path).resolve()

            if not self._is_project_app(app_path):
                continue

            labels.append(app_config.label)

        return labels

    def _remove_project_migrations(self):
        for app_config in apps.get_app_configs():
            app_path = Path(app_config.path).resolve()

            if not self._is_project_app(app_path):
                continue

            migrations_path = app_path / "migrations"

            if not migrations_path.exists():
                migrations_path.mkdir(parents=True)
                (migrations_path / "__init__.py").touch()
                continue

            for path in migrations_path.iterdir():
                if path.name == "__init__.py":
                    continue

                if path.is_dir():
                    rmtree(path)
                    continue

                if path.suffix in {".py", ".pyc"}:
                    path.unlink()

            self.stdout.write(
                f"Очищены миграции: {app_config.label}"
            )

    def _remove_python_cache(self):
        base_dir = Path(settings.BASE_DIR)

        for path in base_dir.rglob("__pycache__"):
            rmtree(path, ignore_errors=True)

    def _is_project_app(self, app_path):
        base_dir = Path(settings.BASE_DIR).resolve()

        try:
            app_path.relative_to(base_dir)
        except ValueError:
            return False

        return ".venv" not in app_path.parts

    def _check_required_tables(self):
        connection = connections["default"]
        tables = set(
            connection.introspection.table_names()
        )

        required_tables = {
            "users_user",
            "users_permission",
        }

        missing_tables = required_tables - tables

        if missing_tables:
            missing = ", ".join(
                sorted(missing_tables)
            )

            raise RuntimeError(
                f"После migrate отсутствуют таблицы: {missing}"
            )