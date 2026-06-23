from backend.generic.models.DynamicValue import (
    DynamicValue,
)


def test_orphans():

    count = 0

    for value in (

        DynamicValue.objects.all()

    ):

        if (

            value.content_object

            is None

        ):

            count += 1

    assert (

        count

        == 0

    )