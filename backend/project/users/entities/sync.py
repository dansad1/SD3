from backend.project.companies.models import Company


def sync_user(user):
    print("=" * 80)

    company = user.get_value("company")

    print("TYPE:", type(company))
    print("VALUE:", repr(company))

    if isinstance(company, dict):
        print("DICT")
        company = Company.objects.filter(
            pk=company.get("value"),
        ).first()

    elif isinstance(company, str):
        print("STRING")
        print("RAW:", company)
        raise RuntimeError(
            f"COMPANY STRING = {company!r}"
        )

    elif isinstance(company, int):
        print("INT")
        company = Company.objects.filter(
            pk=company,
        ).first()

    else:
        print("OTHER:", type(company))