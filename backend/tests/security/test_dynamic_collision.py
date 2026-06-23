from backend.project.users.models import (
    UserField,
)


def test_reserved_name():

    field = UserField(

        name="is_superuser",

        label="x",

    )

    try:

        field.full_clean()

    except Exception:

        return

    assert False