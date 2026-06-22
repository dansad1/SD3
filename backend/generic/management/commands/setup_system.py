from django.core.management import call_command
from django.core.management.base import BaseCommand

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

    help = "Setup system"

    def handle(
        self,
        *args,
        **kwargs,
    ):

        # =====================================
        # BOOTSTRAP
        # =====================================

        bootstrap(
            force=True,
        )

        self.stdout.write("")

        self.stdout.write(
            "╔══════════════════════════════════════╗"
        )

        self.stdout.write(
            "║            SETUP SYSTEM             ║"
        )

        self.stdout.write(
            "╚══════════════════════════════════════╝"
        )

        self.stdout.write("")

        # =====================================
        # PERMISSIONS
        # =====================================

        self.stdout.write(
            "🔑 SYNC PERMISSIONS"
        )

        permission_codes = (
            collect_permissions()
        )

        permissions = []

        for code in permission_codes:

            permission, created = (

                Permission.objects

                .get_or_create(

                    code=code,

                    defaults={

                        "name":
                            code,

                        "category":
                            code.split(".")[0],

                    },
                )
            )

            permissions.append(
                permission
            )

            icon = "✔"

            if created:

                icon = "🟢"

            self.stdout.write(

                f"   {icon} {code}"

            )

        self.stdout.write("")

        # =====================================
        # ADMIN ROLE
        # =====================================

        self.stdout.write(

            "🛡 SYNC ADMIN ROLE"

        )

        role, created = (

            UserRole.objects

            .get_or_create(

                code="admin",

                defaults={

                    "name":
                        "Administrator",

                    "is_active":
                        True,

                    "priority":
                        0,

                },
            )
        )

        role.permissions.set(
            permissions
        )

        self.stdout.write(

            f"   ✔ permissions assigned: "

            f"{len(permissions)}"

        )

        self.stdout.write("")

        # =====================================
        # ROOT USER
        # =====================================

        self.stdout.write(

            "👤 SYNC ROOT USER"

        )

        user, created = (

            User.objects

            .get_or_create(

                login="root",

                defaults={

                    "is_active":
                        True,

                    "is_staff":
                        True,

                    "is_superuser":
                        True,

                    "role":
                        role,

                },
            )
        )

        if created:

            user.set_password(
                "root"
            )

            user.save()

            self.stdout.write(

                "   🟢 root user created"

            )

        if user.role_id != role.id:

            user.role = role

            user.save(

                update_fields=[

                    "role",

                ]

            )

        self.stdout.write(

            "   ✔ login      : root"

        )

        self.stdout.write(

            "   ✔ password   : root"

        )

        self.stdout.write("")

        # =====================================
        # FIELDSETS
        # =====================================

        self.stdout.write(

            "📑 SYNC FIELDSETS"

        )

        call_command(

            "sync_user_fieldset",

            verbosity=0,

        )

        call_command(

            "sync_company_fieldset",

            verbosity=0,

        )

        call_command(

            "sync_ticket_fieldset",

            verbosity=0,

        )

        self.stdout.write(

            "   ✔ user"

        )

        self.stdout.write(

            "   ✔ company"

        )

        self.stdout.write(

            "   ✔ ticket"

        )

        self.stdout.write("")

        # =====================================
        # TICKETS
        # =====================================

        # =====================================
        # TICKETS
        # =====================================

        self.stdout.write(

            "🎫 SYNC TICKET DATA"

        )

        call_command(

            "seed_tickets",

            verbosity=0,

        )

        self.stdout.write(

            "   ✔ priorities"

        )

        self.stdout.write(

            "   ✔ statuses"

        )

        self.stdout.write(

            "   ✔ types"

        )

        self.stdout.write("")

        # =====================================
        # NOTIFICATIONS
        # =====================================

        self.stdout.write(

            "🔔 SYNC NOTIFICATIONS"

        )

        call_command(

            "seed_notifications",

            verbosity=0,

        )

        self.stdout.write(

            "   ✔ events"

        )

        self.stdout.write("")

        # =====================================
        # REGISTRY INFO
        # =====================================

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

                "🔥 SYSTEM READY"

            )

        )

        self.stdout.write("")