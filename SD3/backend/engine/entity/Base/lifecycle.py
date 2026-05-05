from SD3.backend.engine.form.Base.FormContext import FormContext


# =========================
# BEFORE SAVE
# =========================

def before_save(ctx: FormContext):
    entity = ctx.entity

    if hasattr(entity, "before_save"):
        result = entity.before_save(ctx)

        # если entity вернул новый ctx → используем
        if result is not None:
            ctx = result

    return ctx


# =========================
# AFTER SAVE
# =========================

def after_save(ctx: FormContext):
    entity = ctx.entity

    if hasattr(entity, "after_save"):
        result = entity.after_save(ctx)

        if result is not None:
            ctx = result

    return ctx