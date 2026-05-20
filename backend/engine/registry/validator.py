def is_valid_entity_class(cls):

    # =============================================
    # ABSTRACT / EMPTY
    # =============================================

    entity = getattr(
        cls,
        "entity",
        None,
    )

    model = getattr(
        cls,
        "model",
        None,
    )

    if not entity:
        return False

    if not model:
        return False

    return True


def validate_duplicate(
    existing,
    new,
    label="Item",
):

    if not existing:
        return

    if (
        existing.__class__
        == new.__class__
    ):
        return

    raise RuntimeError(

        f"{label} already registered: "

        f"{existing.__class__.__name__} "

        f"vs "

        f"{new.__class__.__name__}"
    )