from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from backend.bootstrap import bootstrap
from backend.engine.action.ActionRegistry import actions
from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.matrix.MatrixRegistry import matrix_registry
from backend.project.permissions.collect import (
    collect_permissions,
)
from backend.project.users.models import (
    Permission,
    User,
    UserRole,
)


class Command(BaseCommand):

    help = (
        "Synchronize system configuration, "
        "permissions and seed data"
    )

    @transaction.atomic
    def handle(
        self,
        *args,
        **kwargs,
    ):

        # =====================================================
        # BOOTSTRAP
        # =====================================================

        bootstrap(
            force=True,
        )

        self.stdout.write("")
        self.stdout.write(
            "╔══════════════════════════════════════╗"
        )
        self.stdout.write(
            "║          SYSTEM SYNCHRONIZE         ║"
        )
        self.stdout.write(
            "╚══════════════════════════════════════╝"
        )
        self.stdout.write("")

        # =====================================================
        # PERMISSIONS
        # =====================================================

        self.stdout.write(
            "🔑 SYNC PERMISSIONS"
        )

        permission_codes = sorted(
            collect_permissions()
        )

        permissions = []

        for code in permission_codes:

            permission, created = (
                Permission.objects
                .update_or_create(
                    code=code,
                    defaults={
                        "name": code,
                        "category": code.split(".")[0],
                    },
                )
            )

            permissions.append(
                permission
            )

            self.stdout.write(
                f"   {'🟢' if created else '✔'} {code}"
            )

        deleted, _ = (
            Permission.objects
            .exclude(
                code__in=permission_codes,
            )
            .delete()
        )

        if deleted:
            self.stdout.write(
                f"   🗑 removed: {deleted}"
            )

        self.stdout.write("")

        # =====================================================
        # ADMIN ROLE
        # =====================================================

        self.stdout.write(
            "🛡 SYNC ADMIN ROLE"
        )

        role, created = (
            UserRole.objects
            .update_or_create(
                code="admin",
                defaults={
                    "name": "Administrator",
                    "is_active": True,
                },
            )
        )

        role.permissions.set(
            permissions
        )

        self.stdout.write(
            f"   {'🟢' if created else '✔'} admin"
        )

        self.stdout.write(
            f"   ✔ permissions: {len(permissions)}"
        )

        self.stdout.write("")

        # =====================================================
        # ROOT USER
        # =====================================================

        self.stdout.write(
            "👤 SYNC ROOT USER"
        )

        user, created = (
            User.objects
            .update_or_create(
                login="root",
                defaults={
                    "is_active": True,
                    "is_staff": True,
                    "is_superuser": True,
                    "role": role,
                },
            )
        )

        # Всегда обновляем пароль root
        user.set_password(
            "root"
        )

        user.save(
            update_fields=[
                "password",
            ]
        )

        self.stdout.write(
            f"   {'🟢' if created else '✔'} root"
        )

        self.stdout.write(
            "   ✔ login    : root"
        )

        self.stdout.write(
            "   ✔ password : root"
        )

        self.stdout.write("")

        # =====================================================
        # SEED COMMANDS
        # =====================================================

        commands = [

            # =============================================
            # FIELDSETS
            # =============================================

            "sync_user_fieldset",
            "sync_company_fieldset",
            "sync_ticket_fieldset",

            # =============================================
            # SYSTEM DATA
            # =============================================

            "seed_tickets",
            "seed_notification_events",

        ]

        self.stdout.write(
            "🌱 SYNC SYSTEM DATA"
        )

        for command in commands:

            self.stdout.write(
                f"   ▶ {command}"
            )

            call_command(
                command,
                verbosity=1,
            )

        self.stdout.write("")

        # =====================================================
        # REGISTRY
        # =====================================================

        self.stdout.write(
            "📦 REGISTRY"
        )

        self.stdout.write(
            f"   ✔ entities : "
            f"{len(entity_registry.storage.by_code)}"
        )

        self.stdout.write(
            f"   ✔ actions  : "
            f"{len(actions.storage.by_code)}"
        )

        self.stdout.write(
            f"   ✔ matrix   : "
            f"{len(matrix_registry.storage.by_code)}"
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "🔥 SYSTEM SYNCHRONIZED"
            )
        )

        self.stdout.write("")