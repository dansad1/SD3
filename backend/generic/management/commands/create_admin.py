import os

from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.db import transaction

from backend.project.users.models import (
    User,
    UserRole,
)


class Command(BaseCommand):

    help = (
        "Создаёт системного администратора"
    )

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):
        existing_admin = (
            User.objects
            .filter(
                is_superuser=True,
            )
            .order_by(
                "pk",
            )
            .first()
        )

        if existing_admin:
            self.stdout.write(
                self.style.SUCCESS(
                    (
                        "Администратор уже существует: "
                        f"{existing_admin.login}"
                    )
                )
            )

            return

        login = os.environ.get(
            "DJANGO_ADMIN_LOGIN",
            "",
        ).strip()

        password = os.environ.get(
            "DJANGO_ADMIN_PASSWORD",
            "",
        )

        if not login:
            raise CommandError(
                (
                    "Переменная "
                    "DJANGO_ADMIN_LOGIN "
                    "не указана"
                )
            )

        if not password:
            raise CommandError(
                (
                    "Переменная "
                    "DJANGO_ADMIN_PASSWORD "
                    "не указана"
                )
            )

        try:
            admin_role = (
                UserRole.objects.get(
                    code="admin",
                )
            )

        except UserRole.DoesNotExist as exc:
            raise CommandError(
                (
                    "Системная роль admin "
                    "не создана. Сначала выполните "
                    "setup_system"
                )
            ) from exc

        user, created = (
            User.objects.get_or_create(
                login=login,
            )
        )

        user.role = admin_role
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        update_fields = [
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

        if created:
            user.set_password(
                password,
            )

            update_fields.append(
                "password",
            )

        user.save(
            update_fields=update_fields,
        )

        if created:
            message = (
                "Администратор создан: "
                f"{user.login}"
            )
        else:
            message = (
                "Пользователь получил права "
                "администратора: "
                f"{user.login}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                message
            )
        )