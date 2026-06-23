from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


def test_list_display():

    for entity in (

        entity_registry

        .storage

        .by_code

        .values()

    ):

        names = {

            f.name

            for f

            in entity.get_fields(

                None

            )

        }

        for field in (

            entity.list_display

        ):

            assert (

                field

                in names

            )