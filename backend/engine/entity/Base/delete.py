from django.utils import timezone

from backend.engine.events import (
    emit,
)


# =========================
# SOFT DELETE
# =========================

def soft_delete(
    entity,
    instance,
):

    instance.deleted_at = timezone.now()

    instance.save(
        update_fields=[
            "deleted_at"
        ]
    )


# =========================
# HARD DELETE
# =========================

def hard_delete(
    entity,
    instance,
):

    instance.delete()


# =========================
# STRATEGY
# =========================

def perform_storage_delete(
    entity,
    instance,
):

    if (
        entity.soft_delete
        and hasattr(
            instance,
            "deleted_at",
        )
    ):
        return soft_delete(
            entity,
            instance,
        )

    return hard_delete(
        entity,
        instance,
    )


# =========================
# EVENTS
# =========================

def emit_before_delete(
    entity,
    request,
    instance,
):

    emit(
        "entity.before_delete",
        entity=entity,
        request=request,
        instance=instance,
    )

    emit(
        f"{entity.entity}.before_delete",
        entity=entity,
        request=request,
        instance=instance,
    )


def emit_after_delete(
    entity,
    request,
    instance,
):

    emit(
        "entity.after_delete",
        entity=entity,
        request=request,
        instance=instance,
    )

    emit(
        f"{entity.entity}.after_delete",
        entity=entity,
        request=request,
        instance=instance,
    )


# =========================
# ENTITY HOOKS
# =========================

def call_before_delete(
    entity,
    request,
    instance,
):

    method = getattr(
        entity,
        "before_delete",
        None,
    )

    if method:
        method(
            request,
            instance,
        )


def call_after_delete(
    entity,
    request,
    instance,
):

    method = getattr(
        entity,
        "after_delete",
        None,
    )

    if method:
        method(
            request,
            instance,
        )


# =========================
# MAIN
# =========================

def perform_delete(
    entity,
    request,
    instance,
):

    # -------------------------
    # BEFORE
    # -------------------------

    emit_before_delete(
        entity,
        request,
        instance,
    )

    call_before_delete(
        entity,
        request,
        instance,
    )

    # -------------------------
    # DELETE
    # -------------------------

    perform_storage_delete(
        entity,
        instance,
    )

    # -------------------------
    # AFTER
    # -------------------------

    call_after_delete(
        entity,
        request,
        instance,
    )

    emit_after_delete(
        entity,
        request,
        instance,
    )

    return {
        "status": "ok"
    }