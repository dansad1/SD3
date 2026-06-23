from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


FORBIDDEN = {

    "password",

    "is_superuser",

    "groups",

    "user_permissions",

}


def test_forbidden_fields():

    for entity in (

        entity_registry

        .storage

        .by_code

        .values()

    ):

        fields = {

            f.name

            for f

            in entity.get_fields(

                None

            )

        }

        assert (

            fields

            &

            FORBIDDEN

            == set()

        )