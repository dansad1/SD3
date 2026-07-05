from collections.abc import Iterable


def sync_m2m(
    manager,
    objects,
):
    """
    Синхронизирует M2M.

    Добавляет недостающие.
    Удаляет лишние.

    objects:
        QuerySet
        list
        tuple
        set
    """

    if objects is None:
        objects = []

    if not isinstance(
        objects,
        Iterable,
    ):
        objects = [objects]

    objects = list(objects)

    current = {

        obj.pk

        for obj in (
            manager.all()
        )
    }

    target = {

        obj.pk

        for obj in objects
    }

    #
    # REMOVE
    #

    remove = current - target

    if remove:

        manager.remove(
            *remove,
        )

    #
    # ADD
    #

    add = target - current

    if add:

        manager.add(
            *add,
        )