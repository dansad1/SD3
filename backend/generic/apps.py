import os

from django.apps import AppConfig


class GenericConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "backend.generic"

    def ready(self):

        # ====================================
        # run only in reloader child
        # ====================================

        if os.environ.get("RUN_MAIN") != "true":
            return

        if getattr(self, "_bootstrapped", False):
            return

        self._bootstrapped = True

        from backend.bootstrap import bootstrap

        bootstrap(force=True)