from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management import (
    BaseCommand,
    call_command,
)


class Command(BaseCommand):
    help = "Создание резервной копии базы данных"

    def handle(self, *args, **options):
        backup_dir = (
            Path(settings.BASE_DIR)
            / "backups"
        )

        backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            f"backup_"
            f"{datetime.now():%Y%m%d_%H%M%S}.json"
        )

        backup_file = (
            backup_dir
            / filename
        )

        self.stdout.write(
            f"Создание бэкапа: {backup_file}"
        )

        with backup_file.open(
            "w",
            encoding="utf-8",
        ) as stream:
            call_command(
                "dumpdata",
                "--natural-foreign",
                "--natural-primary",
                "--indent=2",
                stdout=stream,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Бэкап успешно создан:\n{backup_file}"
            )
        )