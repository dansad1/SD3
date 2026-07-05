from collections.abc import Iterable


def add_m2m(
    manager,
    objects,
):
    if objects is None:
        return

    if not isinstance(
        objects,
        Iterable,
    ):
        objects = [objects]

    manager.add(
        *objects,
    )
