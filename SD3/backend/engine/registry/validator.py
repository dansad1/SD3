from SD3.backend.engine.entity.Base.BaseEntity import BaseEntity


def is_valid_entity_class(cls):
    if cls is BaseEntity:
        return False

    return bool(
        getattr(cls, "entity", None)
        and getattr(cls, "model", None)
    )


def validate_duplicate(existing, new, label="Item"):
    if not existing:
        return

    if existing.__class__ == new.__class__:
        return

    raise RuntimeError(
        f"{label} already registered: "
        f"{existing.__class__.__name__} vs {new.__class__.__name__}"
    )