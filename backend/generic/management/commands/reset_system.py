from django.conf import settings
from django.core.management import (
    BaseCommand,
    CommandError,
    call_command,
)
from django.db import connections


class Command(BaseCommand):

    help = (
        "Полностью пересоздаёт локальную "
        "PostgreSQL-базу с нуля или "
        "из последнего бэкапа"
    )

    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--yes",
            action="store_true",
            help=(
                "Не запрашивать подтверждение"
            ),
        )

        parser.add_argument(
            "--clean",
            action="store_true",
            help="Создать чистую базу",
        )

        parser.add_argument(
            "--restore-latest",
            action="store_true",
            help=(
                "Восстановить последний бэкап"
            ),
        )

        parser.add_argument(
            "--seed",
            action="store_true",
            help=(
                "Для чистой базы выполнить "
                "seed_all"
            ),
        )

    # =====================================================
    # HANDLE
    # =====================================================

    def handle(
        self,
        *args,
        **options,
    ):
        self._check_environment()
        self._check_options(
            options,
        )

        restore_latest = (
            self._select_reset_mode(
                clean=options["clean"],
                restore_latest=options[
                    "restore_latest"
                ],
                skip_confirmation=options[
                    "yes"
                ],
            )
        )

        self._confirm_reset(
            restore_latest=restore_latest,
            skip_confirmation=options[
                "yes"
            ],
        )

        self._reset_database()

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

        if (
            options["seed"]
            and not restore_latest
        ):
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
                "Система восстановлена "
                "из последнего бэкапа"
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

    def _check_options(
        self,
        options,
    ):
        if (
            options["clean"]
            and options["restore_latest"]
        ):
            raise CommandError(
                (
                    "--clean нельзя использовать "
                    "вместе с --restore-latest"
                )
            )

        if (
            options["seed"]
            and options["restore_latest"]
        ):
            raise CommandError(
                (
                    "--seed нельзя использовать "
                    "вместе с --restore-latest"
                )
            )

        if (
            options["yes"]
            and not options["clean"]
            and not options["restore_latest"]
        ):
            raise CommandError(
                (
                    "При использовании --yes "
                    "необходимо указать --clean "
                    "или --restore-latest"
                )
            )

    # =====================================================
    # ENVIRONMENT
    # =====================================================

    def _check_environment(
        self,
    ):
        if not settings.DEBUG:
            raise CommandError(
                (
                    "reset_system запрещён "
                    "при DEBUG=False"
                )
            )

        database = (
            settings.DATABASES[
                "default"
            ]
        )

        if (
            database["ENGINE"]
            != "django.db.backends.postgresql"
        ):
            raise CommandError(
                (
                    "reset_system поддерживает "
                    "только PostgreSQL"
                )
            )

        if not database.get("NAME"):
            raise CommandError(
                (
                    "Имя базы PostgreSQL "
                    "не указано"
                )
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
                (
                    "Не выбран режим "
                    "пересоздания системы"
                )
            )

        self.stdout.write("")
        self.stdout.write(
            "Как пересоздать систему?"
        )
        self.stdout.write(
            "  1 — Чистая база"
        )
        self.stdout.write(
            (
                "  2 — Восстановить "
                "последний бэкап"
            )
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
                    (
                        "Введите 1 для чистой "
                        "базы или 2 для "
                        "восстановления бэкапа"
                    )
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
                "Все данные PostgreSQL будут "
                "удалены, после чего будет "
                "восстановлен последний бэкап."
            )
        else:
            mode = (
                "Все данные PostgreSQL будут "
                "удалены, после чего будет "
                "создана чистая система."
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

        if (
            answer.strip().lower()
            != "yes"
        ):
            raise CommandError(
                "Операция отменена"
            )

    # =====================================================
    # DATABASE
    # =====================================================

    def _close_connections(
        self,
    ):
        for connection in (
            connections.all()
        ):
            connection.close()

    def _reset_database(
        self,
    ):
        self._close_connections()

        connection = connections[
            "default"
        ]

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    (
                        "DROP SCHEMA IF EXISTS "
                        "public CASCADE"
                    )
                )

                cursor.execute(
                    "CREATE SCHEMA public"
                )

        except Exception as exc:
            raise CommandError(
                (
                    "Не удалось очистить "
                    "PostgreSQL-базу"
                )
            ) from exc

        finally:
            self._close_connections()

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "Схема PostgreSQL "
                    "полностью очищена"
                )
            )
        )

    # =====================================================
    # TABLE CHECK
    # =====================================================

    def _check_required_tables(
        self,
    ):
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
                    (
                        "Критичные таблицы "
                        "созданы"
                    )
                )
            )

            return

        missing = ", ".join(
            sorted(
                missing_tables
            )
        )

        raise CommandError(
            (
                "После migrate отсутствуют "
                f"таблицы: {missing}"
            )
        )