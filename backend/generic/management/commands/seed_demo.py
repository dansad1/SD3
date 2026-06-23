# backend/generic/management/commands/seed_demo.py

import random
from types import SimpleNamespace

from faker import Faker

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction
from faker.decode import unidecode

from backend.bootstrap import bootstrap

from backend.generic.models.DynamicValue import (
    DynamicValue,
)

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
)

fake = Faker("ru_RU")

PASSWORD = "12345"

PASSWORD_HASH = make_password(
    PASSWORD
)

COMPANIES = 70

USERS = 300


DEPARTMENTS = [

    "IT",

    "Поддержка",

    "Продажи",

    "Бухгалтерия",

    "HR",

]


class Command(
    BaseCommand
):

    help = "Seed demo data"

    # =====================================================
    # HELPERS
    # =====================================================

    def make_phone(

        self,

    ):

        return (

            "+79"

            +

            str(

                random.randint(

                    100000000,

                    999999999,

                )

            )

        )

    def make_login(

        self,

        index,

    ):

        first = fake.first_name()

        last = fake.last_name()

        login = (

            first[0]

            +

            "."

            +

            last

        )

        login = (

            unidecode(

                login

            )

            .lower()

        )

        login = "".join(

            c

            for c

            in login

            if (

                c.isalnum()

                or

                c == "."

            )

        )

        login = (

            f"{login}.{index}"

        )

        return (

            first,

            last,

            login,

        )

    # =====================================================
    # HANDLE
    # =====================================================

    @transaction.atomic
    def handle(

        self,

        *args,

        **kwargs,

    ):

        self.stdout.write(

            "📦 bootstrap"

        )

        bootstrap(

            force=True,

        )

        # ==========================================
        # CLEANUP
        # ==========================================

        self.stdout.write(

            "🧹 cleanup"

        )

        DynamicValue.objects.all().delete()

        User.objects.exclude(

            login="root",

        ).delete()

        Company.objects.all().delete()

        # ==========================================
        # SETUP
        # ==========================================

        request = SimpleNamespace()

        request.GET = {

            "fieldset":

                "default"

        }

        company_entity = (

            CompanyEntity()

        )

        user_entity = (

            UserEntity()

        )

        company_fieldset = (

            CompanyFieldSet.objects

            .get(

                code="default"

            )

        )

        user_fieldset = (

            UserFieldSet.objects

            .get(

                code="default"

            )

        )

        companies = []

        # ==========================================
        # COMPANIES
        # ==========================================

        self.stdout.write(

            "🏢 Компании"

        )

        company_template = Company(

            fieldset=company_fieldset

        )

        company_fields = {

            field.name: field

            for field

            in

            company_entity.get_fields(

                request=request,

                obj=company_template,

            )

        }

        for i in range(

            COMPANIES

        ):

            company = (

                Company.objects

                .create(

                    fieldset=company_fieldset

                )

            )

            company_name = (

                fake.company()

            )

            values = {

                "name":

                    company_name,

                "full_name":

                    f'ООО "{company_name}"',

                "inn":

                    None

                    if random.random()

                       < 0.05

                    else

                    fake.numerify(

                        "##########"

                    ),

                "kpp":

                    fake.numerify(

                        "#########"

                    ),

                "ogrn":

                    fake.numerify(

                        "#############"

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

                    f"Д-{1000+i}",

                "contract_date":

                    fake.date_between(

                        "-5y",

                        "today",

                    ),

            }

            for name, value in (

                values.items()

            ):

                field = (

                    company_fields.get(

                        name

                    )

                )

                if not field:

                    continue

                try:

                    field.set_value(

                        company,

                        value,

                    )

                except Exception as e:

                    self.stdout.write(

                        self.style.ERROR(

                            f"{name}: {e}"

                        )

                    )

                    raise

            companies.append(

                company

            )

        self.stdout.write(

            self.style.SUCCESS(

                f"✔ компаний {len(companies)}"

            )

        )

        # ==========================================
        # USERS
        # ==========================================

        self.stdout.write(

            "👤 Пользователи"

        )

        user_fields = {

            field.name: field

            for field

            in

            user_entity.get_fields(

                request=request,

            )

        }

        for i in range(

            USERS

        ):

            first_name, last_name, login = (

                self.make_login(

                    i

                )

            )

            user = (

                User.objects

                .create(

                    login=login,

                    password=PASSWORD_HASH,

                    fieldset=user_fieldset,

                    is_active=True,

                )

            )

            values = {

                "full_name":

                    (

                        f"{first_name} "

                        f"{last_name}"

                    ),

                "email":

                    (

                        f"{login}"

                        "@mail.ru"

                    ),

                "phone":

                    None

                    if random.random()

                       < 0.10

                    else

                    self.make_phone(),

                "telegram":

                    None

                    if random.random()

                       < 0.20

                    else

                    "@"

                    +

                    fake.user_name(),

                "department":

                    random.choice(

                        DEPARTMENTS

                    ),

            }

            if companies:

                values[

                    "company"

                ] = random.choice(

                    companies

                )

            for name, value in (

                values.items()

            ):

                field = (

                    user_fields.get(

                        name

                    )

                )

                if not field:

                    continue

                try:

                    field.set_value(

                        user,

                        value,

                    )

                except Exception as e:

                    self.stdout.write(

                        self.style.ERROR(

                            f"{name}: {e}"

                        )

                    )

                    raise

        self.stdout.write(

            self.style.SUCCESS(

                f"✔ пользователей {USERS}"

            )

        )

        self.stdout.write(

            self.style.SUCCESS(

                f"✔ пароль {PASSWORD}"

            )

        )

        self.stdout.write(

            self.style.SUCCESS(

                "🔥 seed complete"

            )

        )