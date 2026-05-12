from backend.engine.entity.EntityRegistry import entity_registry


# =========================
# ENTITY RESOLVE
# =========================

def resolve_entity(resource):
    if getattr(resource, "entity", None):
        return entity_registry.get(resource.entity)
    return None


# =========================
# FIELD ACCESS POLICY
# =========================

def allow_field(resource, entity, name: str):
    """
    Приоритет:
    1. resource.should_include_field
    2. entity.should_include_in_list
    3. default True
    """

    if hasattr(resource, "should_include_field"):
        return resource.should_include_field(name)

    if entity and hasattr(entity, "should_include_in_list"):
        return entity.should_include_in_list(name)

    return True