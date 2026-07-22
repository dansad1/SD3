import random
from types import SimpleNamespace

from django.contrib.auth.hashers import (
    make_password,
)
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.db import transaction
from faker import Faker
from faker.decode import unidecode

from backend.bootstrap import bootstrap
from backend.project.companies.entities.CompanyEntity import (
    CompanyEntity,
)
from backend.project.companies.models import (
    Company,
    CompanyFieldSet,
)
from backend.project.users.entities.UserEntity import (
    UserEntity,
)
from backend.project.users.models import (
    User,
    UserFieldSet,
    UserRole,
)


fake = Faker(
    "ru_RU",
)


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

    # =====================================================
    # ARGUMENTS
    # =====================================================

    def add_arguments(
        self,
        parser,
    ):
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

    # =====================================================
    # HELPERS
    # =====================================================

    def make_phone(
        self,
    ):
        return (
            f"+79"
            f"{random.randint(100000000, 999999999)}"
        )

    def make_login(
        self,
        index,
    ):
        first_name = fake.first_name()

        last_name = fake.last_name()

        login = (
            f"{first_name[0]}."
            f"{last_name}"
        )

        login = unidecode(
            login,
        ).lower()

        login = "".join(
            char
            for char in login
            if (
                char.isalnum()
                or char == "."
            )
        )

        return (
            first_name,
            last_name,
            f"{login}.{index}",
        )

    # =====================================================
    # REQUEST
    # =====================================================

    def get_request(
        self,
    ):
        admin = (
            User.objects
            .filter(
                is_superuser=True,
                is_active=True,
            )
            .order_by(
                "pk",
            )
            .first()
        )

        if admin is None:

            raise CommandError(
                (
                    "Активный администратор не найден. "
                    "Сначала выполните команду "
                    "python manage.py create_admin"
                )
            )

        request = SimpleNamespace()

        request.GET = {
            "fieldset": "default",
        }

        request.user = admin

        return request

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(
        self,
    ):
        self.stdout.write(
            "🧹 cleanup"
        )

        deleted_users, _ = (
            User.objects
            .filter(
                is_superuser=False,
            )
            .delete()
        )

        deleted_companies, _ = (
            Company.objects
            .all()
            .delete()
        )

        self.stdout.write(
            (
                "   удалено пользователей: "
                f"{deleted_users}"
            )
        )

        self.stdout.write(
            (
                "   удалено компаний: "
                f"{deleted_companies}"
            )
        )

    # =====================================================
    # FIELDS
    # =====================================================

    def get_company_fields(
        self,
        request,
        fieldset,
    ):
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

    def get_user_fields(
        self,
        request,
    ):
        entity = UserEntity()

        return {
            field.name: field
            for field in entity.get_fields(
                request=request,
            )
        }

    # =====================================================
    # DYNAMIC VALUES
    # =====================================================

    def set_dynamic_values(
        self,
        obj,
        fields,
        values,
    ):
        for name, value in values.items():

            field = fields.get(
                name,
            )

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

    # =====================================================
    # COMPANIES
    # =====================================================

    def seed_companies(
        self,
        count,
        request,
        fieldset,
    ):
        self.stdout.write(
            "🏢 Компании"
        )

        fields = self.get_company_fields(
            request=request,
            fieldset=fieldset,
        )

        companies = []

        for index in range(
            count,
        ):
            company = (
                Company.objects.create(
                    fieldset=fieldset,
                )
            )

            company_name = fake.company()

            values = {
                "name":
                    company_name,

                "full_name":
                    f'ООО "{company_name}"',

                "inn": (
                    None
                    if random.random() < 0.05
                    else fake.numerify(
                        "##########",
                    )
                ),

                "kpp":
                    fake.numerify(
                        "#########",
                    ),

                "ogrn":
                    fake.numerify(
                        "#############",
                    ),

                "contact_person":
                    fake.name(),

                "phone":
                    self.make_phone(),

                "email":
                    fake.company_email(),

                "address":
                    fake.address(),

                "contract_number":
                    f"Д-{1000 + index}",

                "contract_date":
                    fake.date_between(
                        start_date="-5y",
                        end_date="today",
                    ),
            }

            self.set_dynamic_values(
                obj=company,
                fields=fields,
                values=values,
            )

            companies.append(
                company,
            )

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "✔ компаний "
                    f"{len(companies)}"
                )
            )
        )

        return companies

    # =====================================================
    # USERS
    # =====================================================

    def seed_users(
        self,
        count,
        password,
        request,
        fieldset,
        companies,
    ):
        self.stdout.write(
            "👤 Пользователи"
        )

        password_hash = make_password(
            password,
        )

        fields = self.get_user_fields(
            request=request,
        )

        roles = {
            role.code: role
            for role in (
                UserRole.objects
                .filter(
                    is_active=True,
                )
            )
        }

        role_pool = (
            ["executor"] * 50
            + ["senior_executor"] * 10
            + ["dispatcher"] * 12
            + ["company_manager"] * 15
            + ["observer"] * 5
            + ["auditor"] * 3
            + ["helpdesk_manager"] * 3
            + ["admin"] * 2
        )

        created_count = 0

        for index in range(
            count,
        ):
            (
                first_name,
                last_name,
                login,
            ) = self.make_login(
                index,
            )

            user = User.objects.create(
                login=login,
                password=password_hash,
                fieldset=fieldset,
                is_active=True,
            )

            values = {
                "full_name": (
                    f"{first_name} "
                    f"{last_name}"
                ),

                "email": (
                    f"{login}@mail.ru"
                ),

                "phone": (
                    None
                    if random.random() < 0.10
                    else self.make_phone()
                ),

                "telegram": (
                    None
                    if random.random() < 0.20
                    else (
                        f"@{fake.user_name()}"
                    )
                ),

                "department":
                    random.choice(
                        DEPARTMENTS,
                    ),
            }

            if companies:

                values["company"] = (
                    random.choice(
                        companies,
                    )
                )

            self.set_dynamic_values(
                obj=user,
                fields=fields,
                values=values,
            )

            role_code = random.choice(
                role_pool,
            )

            role = roles.get(
                role_code,
            )

            if role:

                user.role = role

                user.save(
                    update_fields=[
                        "role",
                    ],
                )

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                (
                    "✔ пользователей "
                    f"{created_count}"
                )
            )
        )

        return created_count

    # =====================================================
    # SUMMARY
    # =====================================================

    def print_summary(
        self,
        companies_count,
        users_count,
        password,
        admin,
    ):
        self.stdout.write(
            ""
        )

        self.stdout.write(
            "══════════════════════════════════════"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "🔥 DEMO DATA SEEDED"
            )
        )

        self.stdout.write(
            "══════════════════════════════════════"
        )

        self.stdout.write(
            f"Companies : {companies_count}"
        )

        self.stdout.write(
            f"Users     : {users_count}"
        )

        self.stdout.write(
            f"Password  : {password}"
        )

        self.stdout.write(
            ""
        )

        self.stdout.write(
            (
                "Administrator untouched: "
                f"{admin.login}"
            )
        )

        self.stdout.write(
            "══════════════════════════════════════"
        )

    # =====================================================
    # HANDLE
    # =====================================================

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):
        companies_count = options[
            "companies"
        ]

        users_count = options[
            "users"
        ]

        password = options[
            "password"
        ]

        if companies_count < 0:

            raise CommandError(
                (
                    "--companies не может "
                    "быть отрицательным"
                )
            )

        if users_count < 0:

            raise CommandError(
                (
                    "--users не может "
                    "быть отрицательным"
                )
            )

        if not password:

            raise CommandError(
                "--password не может быть пустым"
            )

        self.stdout.write(
            "📦 bootstrap"
        )

        bootstrap(
            force=True,
        )

        # Сначала получаем администратора.
        # Если его нет, команда завершится до очистки.
        request = self.get_request()

        admin = request.user

        self.cleanup()

        company_fieldset = (
            CompanyFieldSet.objects.get(
                code="default",
            )
        )

        user_fieldset = (
            UserFieldSet.objects.get(
                code="default",
            )
        )

        companies = self.seed_companies(
            count=companies_count,
            request=request,
            fieldset=company_fieldset,
        )

        created_users = self.seed_users(
            count=users_count,
            password=password,
            request=request,
            fieldset=user_fieldset,
            companies=companies,
        )

        self.print_summary(
            companies_count=len(
                companies,
            ),
            users_count=created_users,
            password=password,
            admin=admin,
        )