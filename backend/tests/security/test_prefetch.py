from django.test.utils import (
    CaptureQueriesContext,
)

from django.db import connection


def test_query_count(

        client,

):

    with CaptureQueriesContext(

            connection

    ) as ctx:

        client.get(

            "/api/entity/user/list/"

        )

    assert (

            len(

                ctx

            )

            < 15

    )