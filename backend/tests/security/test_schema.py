from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


def test_schema():

    for entity in (

        entity_registry

        .storage

        .by_code

        .values()

    ):

        request = None

        entity.get_fields(

            request

        )