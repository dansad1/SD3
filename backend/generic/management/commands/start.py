import subprocess
import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Запуск системы"

    def handle(self, *args, **kwargs):
        self.stdout.write("")
        self.stdout.write("🔥 START SYSTEM")
        self.stdout.write("")

        self.stdout.write("→ migrate")

        call_command(
            "migrate",
            interactive=False,
        )

        self.stdout.write("→ runserver")
        self.stdout.write("")

        subprocess.run(
            [
                sys.executable,
                "manage.py",
                "runserver",
                "8000",
            ],
            check=False,
        )