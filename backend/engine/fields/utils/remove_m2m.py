from collections.abc import Iterable


def remove_m2m(
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

    manager.remove(
        *objects,
    )