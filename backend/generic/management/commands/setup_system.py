from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from backend.bootstrap import bootstrap
from backend.engine.action.ActionRegistry import actions
from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.matrix.MatrixRegistry import matrix_registry
from backend.project.permissions.collect import collect_permissions
from backend.project.users.models import (
    Permission,
    User,
    UserRole,
)


class Command(BaseCommand):
    help = (
        "Synchronize system configuration, "
        "permissions, roles and system data"
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

        for code in permission_codes:
            permission, created = (
                Permission.objects.update_or_create(
                    code=code,
                    defaults={
                        "name": code,
                        "category": code.split(".")[0],
                    },
                )
            )

            self.stdout.write(
                f"   {'🟢' if created else '✔'} "
                f"{permission.code}"
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
        # ROLES
        # =====================================================

        self.stdout.write(
            "🛡 SYNC SYSTEM ROLES"
        )

        call_command(
            "sync_roles",
            verbosity=1,
        )

        self.stdout.write("")

        # =====================================================
        # ROOT USER
        # =====================================================

        self.stdout.write(
            "👤 SYNC ROOT USER"
        )

        try:
            admin_role = UserRole.objects.get(
                code="admin",
            )
        except UserRole.DoesNotExist as exc:
            raise RuntimeError(
                "Системная роль admin не создана"
            ) from exc

        user, created = (
            User.objects.update_or_create(
                login="root",
                defaults={
                    "is_active": True,
                    "is_staff": True,
                    "is_superuser": True,
                    "role": admin_role,
                },
            )
        )

        update_fields = []

        if user.role_id != admin_role.pk:
            user.role = admin_role
            update_fields.append(
                "role"
            )

        if not user.is_active:
            user.is_active = True
            update_fields.append(
                "is_active"
            )

        if not user.is_staff:
            user.is_staff = True
            update_fields.append(
                "is_staff"
            )

        if not user.is_superuser:
            user.is_superuser = True
            update_fields.append(
                "is_superuser"
            )

        if created:
            user.set_password(
                "root"
            )
            update_fields.append(
                "password"
            )

        if update_fields:
            user.save(
                update_fields=sorted(
                    set(update_fields)
                ),
            )

        self.stdout.write(
            f"   {'🟢' if created else '✔'} root"
        )

        self.stdout.write(
            "   ✔ login: root"
        )

        if created:
            self.stdout.write(
                "   ✔ initial password: root"
            )
        else:
            self.stdout.write(
                "   ✔ password unchanged"
            )

        self.stdout.write("")

        # =====================================================
        # SYSTEM COMMANDS
        # =====================================================

        commands = [
            "sync_user_fieldset",
            "sync_company_fieldset",
            "sync_ticket_fieldset",
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
            "   ✔ entities : "
            f"{len(entity_registry.storage.by_code)}"
        )

        self.stdout.write(
            "   ✔ actions  : "
            f"{len(actions.storage.by_code)}"
        )

        self.stdout.write(
            "   ✔ matrix   : "
            f"{len(matrix_registry.storage.by_code)}"
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "🔥 SYSTEM SYNCHRONIZED"
            )
        )

        self.stdout.write("")