import random
from types import SimpleNamespace

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from faker.decode import unidecode

from backend.bootstrap import bootstrap
from backend.generic.models.DynamicValue import DynamicValue
from backend.project.companies.entities.CompanyEntity import CompanyEntity
from backend.project.companies.models import Company, CompanyFieldSet
from backend.project.users.entities.UserEntity import UserEntity
from backend.project.users.models import User, UserFieldSet

fake = Faker("ru_RU")

DEFAULT_PASSWORD = "12345"
DEFAULT_COMPANIES = 70
DEFAULT_USERS = 300

DEPARTMENTS = [
    "IT",
    "Поддержка",
    "Продажи",
    "Бухгалтерия",
    "HR",
]


class Command(BaseCommand):
    help = "Seed demo data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--companies",
            type=int,
            default=DEFAULT_COMPANIES,
        )
        parser.add_argument(
            "--users",
            type=int,
            default=DEFAULT_USERS,
        )
        parser.add_argument(
            "--password",
            type=str,
            default=DEFAULT_PASSWORD,
        )

    def make_phone(self):
        return f"+79{random.randint(100000000, 999999999)}"

    def make_login(self, index):
        first_name = fake.first_name()
        last_name = fake.last_name()

        login = f"{first_name[0]}.{last_name}"
        login = unidecode(login).lower()

        login = "".join(
            char
            for char in login
            if char.isalnum() or char == "."
        )

        return first_name, last_name, f"{login}.{index}"

    def get_request(self):
        request = SimpleNamespace()
        request.GET = {
            "fieldset": "default",
        }
        return request

    def cleanup(self):
        self.stdout.write("🧹 cleanup")

        DynamicValue.objects.all().delete()

        User.objects.exclude(
            login="root",
        ).delete()

        Company.objects.all().delete()

    def get_company_fields(self, request, fieldset):
        entity = CompanyEntity()

        template = Company(
            fieldset=fieldset,
        )

        return {
            field.name: field
            for field in entity.get_fields(
                request=request,
                obj=template,
            )
        }

    def get_user_fields(self, request):
        entity = UserEntity()

        return {
            field.name: field
            for field in entity.get_fields(
                request=request,
            )
        }

    def set_dynamic_values(self, obj, fields, values):
        for name, value in values.items():
            field = fields.get(name)

            if not field:
                continue

            try:
                field.set_value(
                    obj,
                    value,
                )
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(
                        f"{name}: {exc}"
                    )
                )
                raise

    def seed_companies(self, count, request, fieldset):
        self.stdout.write("🏢 Компании")

        fields = self.get_company_fields(
            request=request,
            fieldset=fieldset,
        )

        companies = []

        for index in range(count):
            company = Company.objects.create(
                fieldset=fieldset,
            )

            company_name = fake.company()

            values = {
                "name": company_name,
                "full_name": f'ООО "{company_name}"',
                "inn": (
                    None
                    if random.random() < 0.05
                    else fake.numerify("##########")
                ),
                "kpp": fake.numerify("#########"),
                "ogrn": fake.numerify("#############"),
                "contact_person": fake.name(),
                "phone": self.make_phone(),
                "email": fake.company_email(),
                "address": fake.address(),
                "contract_number": f"Д-{1000 + index}",
                "contract_date": fake.date_between(
                    "-5y",
                    "today",
                ),
            }

            self.set_dynamic_values(
                obj=company,
                fields=fields,
                values=values,
            )

            companies.append(company)

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ компаний {len(companies)}"
            )
        )

        return companies

    def seed_users(
        self,
        count,
        password,
        request,
        fieldset,
        companies,
    ):
        self.stdout.write("👤 Пользователи")

        password_hash = make_password(password)

        fields = self.get_user_fields(
            request=request,
        )

        for index in range(count):
            first_name, last_name, login = self.make_login(
                index,
            )

            user = User.objects.create(
                login=login,
                password=password_hash,
                fieldset=fieldset,
                is_active=True,
            )

            values = {
                "full_name": f"{first_name} {last_name}",
                "email": f"{login}@mail.ru",
                "phone": (
                    None
                    if random.random() < 0.10
                    else self.make_phone()
                ),
                "telegram": (
                    None
                    if random.random() < 0.20
                    else f"@{fake.user_name()}"
                ),
                "department": random.choice(DEPARTMENTS),
            }

            if companies:
                values["company"] = random.choice(
                    companies,
                )

            self.set_dynamic_values(
                obj=user,
                fields=fields,
                values=values,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ пользователей {count}"
            )
        )

    def print_summary(self, companies_count, users_count, password):
        self.stdout.write("")
        self.stdout.write("══════════════════════════════════════")
        self.stdout.write(
            self.style.SUCCESS(
                "🔥 DEMO DATA SEEDED"
            )
        )
        self.stdout.write("══════════════════════════════════════")
        self.stdout.write(f"Companies : {companies_count}")
        self.stdout.write(f"Users     : {users_count}")
        self.stdout.write(f"Password  : {password}")
        self.stdout.write("")
        self.stdout.write("Root user : untouched")
        self.stdout.write("══════════════════════════════════════")

    @transaction.atomic
    def handle(self, *args, **options):
        companies_count = options["companies"]
        users_count = options["users"]
        password = options["password"]

        self.stdout.write("📦 bootstrap")

        bootstrap(
            force=True,
        )

        self.cleanup()

        request = self.get_request()

        company_fieldset = CompanyFieldSet.objects.get(
            code="default",
        )

        user_fieldset = UserFieldSet.objects.get(
            code="default",
        )

        companies = self.seed_companies(
            count=companies_count,
            request=request,
            fieldset=company_fieldset,
        )

        self.seed_users(
            count=users_count,
            password=password,
            request=request,
            fieldset=user_fieldset,
            companies=companies,
        )

        self.print_summary(
            companies_count=len(companies),
            users_count=users_count,
            password=password,
        )