from django.core.exceptions import ValidationError

from backend.project.users.models.UserListSettings import (
    UserListSettings,
)


def apply_visibility(ctx):

    entity_name = ctx.entity.entity

    # ==========================================
    # RUNTIME FIELDS
    # ==========================================

    runtime_fields = (
        ctx.runtime_fields
        or []
    )

    available_keys = {
        field.name
        for field in runtime_fields
    }

    # ==========================================
    # DEFAULT
    # ==========================================

    default = (
        ctx.entity.list_display
        or list(available_keys)
    )

    # ==========================================
    # SETTINGS
    # ==========================================

    settings = (
        UserListSettings.objects
        .filter(
            user=ctx.request.user,
            entity=entity_name,
        )
        .first()
    )

    visible = None

    if settings:

        raw = settings.visible_fields

        # ======================================
        # VALIDATION
        # ======================================

        if isinstance(raw, list):

            visible = [
                x
                for x in raw
                if (
                    isinstance(x, str)
                    and x in available_keys
                )
            ]

    # ==========================================
    # FALLBACK
    # ==========================================

    if not visible:
        visible = default

    visible_set = set(visible)

    # ==========================================
    # APPLY RUNTIME FIELDS
    # ==========================================

    ctx.runtime_fields = [

        field

        for field in runtime_fields

        if field.name in visible_set
    ]

    # ==========================================
    # APPLY SCHEMA FIELDS
    # ==========================================

    ctx.fields = [

        field

        for field in (
            ctx.fields
            or []
        )

        if field["key"] in visible_set
    ]

    return ctx