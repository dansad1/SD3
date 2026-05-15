import subprocess

from django.core.management import (
    call_command
)

from django.core.management.base import (
    BaseCommand
)


class Command(BaseCommand):

    help = "Full startup"

    def handle(self, *args, **kwargs):

        self.stdout.write("")
        self.stdout.write(
            "🔥 START SYSTEM"
        )

        self.stdout.write("")

        # =====================================
        # MIGRATE
        # =====================================

        self.stdout.write(
            "→ migrate"
        )

        call_command(
            "migrate"
        )

        # =====================================
        # SETUP
        # =====================================

        self.stdout.write(
            "→ setup_system"
        )

        call_command(
            "setup_system"
        )

        # =====================================
        # RUNSERVER
        # =====================================

        self.stdout.write(
            "→ runserver"
        )

        self.stdout.write("")

        subprocess.run([
            "python",
            "manage.py",
            "runserver",
            "8000",
        ])