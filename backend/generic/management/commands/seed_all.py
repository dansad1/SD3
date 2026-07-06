from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):

    help = (
        "Initialize all system dictionaries "
        "and default configuration"
    )

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):

        commands = [

            # =====================================================
            # FIELDSETS
            # =====================================================

            "sync_user_fieldset",
            "sync_company_fieldset",
            "sync_ticket_fieldset",

            # =====================================================
            # SYSTEM DICTIONARIES
            # =====================================================

            "seed_tickets",
            "seed_notification_events",

            # =====================================================
            # FUTURE
            # =====================================================

            # "seed_services",
            # "seed_roles",
            # "seed_permissions",
            # "seed_templates",
            # "seed_workflows",
            # "seed_lifecycles",

        ]

        for command in commands:

            self.stdout.write(
                self.style.NOTICE(
                    f"==> {command}"
                )
            )

            call_command(command)

        self.stdout.write()

        self.stdout.write(
            self.style.SUCCESS(
                "System successfully initialized."
            )
        )