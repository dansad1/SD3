from backend.engine.form.Base.FormContext import (
    FormContext
)

from backend.engine.events import (
    emit,
)


# =========================
# ENTITY HOOK
# =========================

def call_entity_hook(
    entity,
    hook,
    ctx,
):

    method = getattr(
        entity,
        hook,
        None,
    )

    if not method:
        return ctx

    result = method(ctx)

    return result or ctx


# =========================
# EVENTS
# =========================

def emit_before_save(ctx):

    emit(
        "entity.before_save",
        ctx=ctx,
    )

    emit(
        f"{ctx.entity.entity}.before_save",
        ctx=ctx,
    )

    return ctx


def emit_after_save(ctx):

    emit(
        "entity.after_save",
        ctx=ctx,
    )

    emit(
        f"{ctx.entity.entity}.after_save",
        ctx=ctx,
    )

    return ctx


# =========================
# ENTITY
# =========================

def entity_before_save(ctx):

    return call_entity_hook(
        ctx.entity,
        "before_save",
        ctx,
    )


def entity_after_save(ctx):

    return call_entity_hook(
        ctx.entity,
        "after_save",
        ctx,
    )


# =========================
# PIPELINES
# =========================

BEFORE_SAVE_PIPELINE = [
    emit_before_save,
    entity_before_save,
]

AFTER_SAVE_PIPELINE = [
    emit_after_save,
    entity_after_save,
]


# =========================
# MAIN
# =========================

def before_save(
    ctx: FormContext,
):

    for step in BEFORE_SAVE_PIPELINE:
        ctx = step(ctx)

    return ctx


def after_save(
    ctx: FormContext,
):

    for step in AFTER_SAVE_PIPELINE:
        ctx = step(ctx)

    return ctx