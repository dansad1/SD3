import os

from django.apps import AppConfig


class GenericConfig(AppConfig):

    default_auto_field = (
        "django.db.models.BigAutoField"
    )

    name = "backend.generic"

    _bootstrapped = False

    def ready(self):

        # already bootstrapped
        if self._bootstrapped:
            return

        self._bootstrapped = True

        # skip autoreloader parent
        if os.environ.get(
            "RUN_MAIN"
        ) != "true":

            return

        from backend.bootstrap import (
            bootstrap
        )

        bootstrap(force=True)