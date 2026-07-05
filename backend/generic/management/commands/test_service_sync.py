from django.core.management.base import BaseCommand

from backend.project.companies.models import (
    Company,
)

from backend.project.services.entities.sync import (
    sync_service,
)

from backend.project.services.models import (
    Service,
)

from backend.project.users.models import (
    User,
    UserField,
    UserFieldValue,
)


class Command(BaseCommand):

    help = "Test service/company/user synchronization"

    def handle(
        self,
        *args,
        **kwargs,
    ):
        company = Company.objects.first()
        service = Service.objects.first()

        if not company:
            self.stdout.write(
                self.style.ERROR("Нет компаний")
            )
            return

        if not service:
            self.stdout.write(
                self.style.ERROR("Нет сервисов")
            )
            return

        user, _ = User.objects.get_or_create(
            login="test_sync",
            defaults={
                "is_active": True,
            },
        )

        field = UserField.objects.get(
            name="company",
        )

        UserFieldValue.objects.update_or_create(
            user=user,
            field=field,
            defaults={
                "value": str(company.pk),
            },
        )

        user.refresh_from_db()

        service.users.remove(user)
        service.companies.remove(company)

        self.stdout.write(
            self.style.WARNING("STEP 1: BEFORE")
        )

        self.stdout.write(f"User: {user.login}")
        self.stdout.write(f"Company: {company}")
        self.stdout.write(f"Service: {service}")

        self.stdout.write(
            f"User company raw value: "
            f"{user.get_value('company')}"
        )

        self.stdout.write(
            f"Company in service: "
            f"{service.companies.filter(pk=company.pk).exists()}"
        )

        self.stdout.write(
            f"User in service: "
            f"{service.users.filter(pk=user.pk).exists()}"
        )

        self.stdout.write(
            self.style.WARNING("STEP 2: ADD COMPANY TO SERVICE")
        )

        service.companies.add(company)

        self.stdout.write(
            f"Company in service: "
            f"{service.companies.filter(pk=company.pk).exists()}"
        )

        self.stdout.write(
            self.style.WARNING("STEP 3: SYNC SERVICE")
        )

        sync_service(service)

        service.refresh_from_db()

        self.stdout.write(
            self.style.SUCCESS("STEP 4: AFTER")
        )

        self.stdout.write(
            f"User in service: "
            f"{service.users.filter(pk=user.pk).exists()}"
        )

        self.stdout.write(
            "Service users: "
            + str(
                list(
                    service.users.values_list(
                        "login",
                        flat=True,
                    )
                )
            )
        )

        self.stdout.write(
            self.style.WARNING("STEP 5: REMOVE COMPANY AND SYNC")
        )

        service.companies.remove(company)

        sync_service(service)

        service.refresh_from_db()

        self.stdout.write(
            f"User in service after remove: "
            f"{service.users.filter(pk=user.pk).exists()}"
        )

        self.stdout.write(
            "Service users after remove: "
            + str(
                list(
                    service.users.values_list(
                        "login",
                        flat=True,
                    )
                )
            )
        )