import logging

from django.core.exceptions import (
    PermissionDenied,
    ValidationError as DjangoValidationError,
)
from django.db import transaction
from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
)

from backend.engine.entity.Base.lifecycle import (
    after_save,
    before_save,
)
from backend.engine.entity.EntityRegistry import (
    entity_registry,
)
from backend.engine.form.Base.errors import (
    validation_error_to_dict,
)
from backend.engine.form.Base.FormContext import (
    FormContext,
)
from backend.engine.form.Base.initial import (
    apply_query_initial,
)
from backend.engine.form.Base.instance import (
    load_instance,
)
from backend.engine.form.Base.normalize import (
    normalize,
)
from backend.engine.form.Base.save import (
    save,
)
from backend.engine.form.Base.schema import (
    build_schema,
)
from backend.engine.form.Base.serialize import (
    serialize,
)
from backend.engine.form.Base.special_save import (
    save_special_fields,
)
from backend.engine.utils.permissions import (
    has_permission,
)

logger = logging.getLogger(__name__)


def apply_payload(ctx: FormContext):
    ctx.data = (
        ctx.payload
        or {}
    ).copy()

    setattr(
        ctx.request,
        "_form_payload",
        ctx.data,
    )

    return ctx


# =========================================================
# SECURITY
# =========================================================

def filter_editable_fields(
        ctx: FormContext,
):
    editable = {
        field.name
        for field in (
            ctx.runtime_fields
            or []
        )
        if getattr(
            field,
            "access_level",
            "edit",
        ) == "edit"
    }

    ctx.data = {
        key: value
        for key, value in (
            ctx.data
            or {}
        ).items()
        if key in editable
    }

    return ctx


# =========================================================
# PERMISSION
# =========================================================

def validate_entity(
        ctx: FormContext,
):
    ctx.data = ctx.entity.validate(
        request=ctx.request,
        payload=ctx.data,
        instance=ctx.instance,
    )

    return ctx


def check_permission(
        ctx: FormContext,
):
    entity = ctx.entity
    request = ctx.request

    action_map = {
        "view": "view",
        "create": "create",
        "edit": "edit",
    }

    action = action_map.get(
        ctx.mode
    )

    if not action:
        raise PermissionDenied

    if not has_permission(
            entity.ctx(request),
            action,
    ):
        raise PermissionDenied

    ctx.capabilities = (
        entity
        .get_capabilities_for_user(
            request
        )
    )

    return ctx


# =========================================================
# RUNTIME FIELDS
# =========================================================

def load_runtime_fields(
        ctx: FormContext,
):
    runtime_fields = ctx.entity.get_fields(
        request=ctx.request,
        obj=ctx.instance,
    )

    ctx.runtime_fields = (
        runtime_fields
        or []
    )

    ctx.field_map = {
        field.name: field
        for field in ctx.runtime_fields
    }

    return ctx


def debug_data(
        ctx: FormContext,
):
    logger.debug(
        "FORM DATA AFTER NORMALIZE: %s",
        ctx.data,
    )

    return ctx


# =========================================================
# PIPELINES
# =========================================================

BUILD_PIPELINE = [
    check_permission,
    load_instance,
    load_runtime_fields,
    build_schema,
    serialize,
    apply_query_initial,
]

SUBMIT_PIPELINE = [
    check_permission,
    load_instance,
    apply_payload,
    load_runtime_fields,
    build_schema,
    filter_editable_fields,
    normalize,
    debug_data,
    validate_entity,
    before_save,
    save_special_fields,
    save,
    after_save,
]


class BaseForm:
    code = None
    entity = None

    def get_entity(self):
        if self.entity:
            return self.entity

        entity_name = self.code.split(".")[0]

        return entity_registry.get(
            entity_name
        )

    def resolve_pk(
            self,
            request,
            mode,
            pk,
    ):
        entity = self.get_entity()

        if hasattr(
                entity,
                "resolve_pk",
        ):
            return entity.resolve_pk(
                request,
                mode,
                pk,
            )

        return pk

    def build(
            self,
            request,
            mode,
            pk=None,
    ):
        pk = self.resolve_pk(
            request,
            mode,
            pk,
        )

        if (
            pk
            and mode == "create"
        ):
            mode = "edit"

        ctx = FormContext(
            form=self,
            request=request,
            mode=mode,
            pk=pk,
        )

        for step in BUILD_PIPELINE:
            step(ctx)

        return {
            "entity": ctx.entity.entity,
            "fields": ctx.fields,
            "initial": ctx.data,
            "capabilities": ctx.capabilities,
        }

    @transaction.atomic
    def submit(
            self,
            request,
            mode,
            payload,
            pk=None,
    ):
        if mode == "view":
            raise PermissionDenied

        pk = self.resolve_pk(
            request,
            mode,
            pk,
        )

        ctx = FormContext(
            form=self,
            request=request,
            mode=mode,
            pk=pk,
            payload=payload,
        )

        try:
            for step in SUBMIT_PIPELINE:
                logger.debug(
                    "FORM STEP: %s",
                    step.__name__,
                )
                step(ctx)

        except (
            DjangoValidationError,
            DRFValidationError,
        ) as exc:
            return {
                "status": "error",
                "errors": validation_error_to_dict(
                    exc
                ),
            }

        except Exception:
            logger.exception(
                "Unhandled exception in form submit",
                extra={
                    "entity": ctx.entity.entity,
                    "mode": mode,
                    "pk": pk,
                },
            )
            raise

        return {
            "status": "ok",
            "id": ctx.instance.pk,
        }