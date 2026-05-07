# =========================
# SYSTEM
# =========================

def check_system_fields(
    entity,
    name,
):

    return (
        name
        not in entity.system_exclude_fields
    )


# =========================
# EXCLUDE
# =========================

def check_exclude_fields(
    entity,
    name,
):

    if not entity.exclude_fields:
        return True

    return (
        name
        not in entity.exclude_fields
    )


# =========================
# INCLUDE
# =========================

def check_include_fields(
    entity,
    name,
):

    if entity.include_fields is None:
        return True

    return (
        name
        in entity.include_fields
    )


# =========================
# PIPELINE
# =========================

PIPELINE = [
    check_system_fields,
    check_exclude_fields,
    check_include_fields,
]


# =========================
# MAIN
# =========================

def should_include_field_name(
    entity,
    name,
):

    for step in PIPELINE:

        result = step(
            entity,
            name,
        )

        if not result:
            return False

    return True


# =========================
# LIST
# =========================

def should_include_in_list(
    entity,
    name,
):

    return should_include_field_name(
        entity,
        name,
    )