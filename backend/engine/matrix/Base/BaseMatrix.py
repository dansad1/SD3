import json

from rest_framework.exceptions import PermissionDenied

from backend.engine.matrix.Base.MatrixContext import MatrixContext
from backend.engine.matrix.Base.changes import extract_changes
from backend.engine.matrix.Base.data import load_data
from backend.engine.matrix.Base.save import save
from backend.engine.matrix.Base.schema import build_schema
from backend.engine.utils.permissions import has_permission


def build_capabilities(ctx: MatrixContext):
    matrix = ctx.matrix
    request = ctx.request

    actions = [
        "view",
        "edit",
    ]

    ctx.capabilities = {

        action:

            has_permission(

                type(

                    "PermCtx",

                    (),

                    {

                        "request":
                            request,

                        "entity":

                            type(

                                "EntityStub",

                                (),

                                {

                                    "capabilities": {

                                        action:
                                            matrix.capabilities.get(
                                                action,
                                            ),

                                    },

                                },

                            )(),

                    },

                ),

                action,

            )

        for action in actions

    }


def check_permission(
    ctx: MatrixContext,
    action: str,
):
    matrix = ctx.matrix
    request = ctx.request

    perm_code = matrix.capabilities.get(
        action,
    )

    if not perm_code:
        return

    perm_ctx = type(
        "PermCtx",
        (),
        {},
    )()

    perm_ctx.request = request

    perm_ctx.entity = type(
        "EntityStub",
        (),
        {},
    )()

    perm_ctx.entity.capabilities = {

        action:
            perm_code,

    }

    if not has_permission(
        perm_ctx,
        action,
    ):
        raise PermissionDenied


BUILD_PIPELINE = [

    build_capabilities,

    lambda ctx:
        check_permission(
            ctx,
            "view",
        ),

    load_data,

    build_schema,

]


SUBMIT_PIPELINE = [

    build_capabilities,

    lambda ctx:
        check_permission(
            ctx,
            "edit",
        ),

    extract_changes,

    save,

]


class BaseMatrix:

    class Meta:

        code = None

        capabilities = None

    def __init__(self):

        meta = getattr(
            self,
            "Meta",
            None,
        )

        if (

            not meta

            or

            not getattr(
                meta,
                "code",
                None,
            )

        ):

            raise RuntimeError(

                f"{self.__class__.__name__}"
                " must define Meta.code"

            )

        self.code = meta.code

        self.capabilities = (

            getattr(
                meta,
                "capabilities",
                {},
            )

            or

            {}

        )

    def get_context(
        self,
        request,
    ):
        runtime_ctx = getattr(
            request,
            "_matrix_context",
            None,
        )

        if isinstance(
            runtime_ctx,
            dict,
        ):
            return runtime_ctx

        raw = request.GET.get(
            "ctx",
        )

        if not raw:
            return {}

        try:

            ctx = json.loads(
                raw,
            )

        except Exception:

            return {}

        if isinstance(
            ctx,
            dict,
        ):
            return ctx

        return {}

    def get_param(
        self,
        request,
        name,
        default=None,
    ):
        value = request.GET.get(
            name,
        )

        if value is not None:
            return value

        value = getattr(
            request,
            "data",
            {},
        ).get(
            name,
        )

        if value is not None:
            return value

        ctx = self.get_context(
            request,
        )

        return ctx.get(
            name,
            default,
        )

    def build_schema(
        self,
        request,
    ):
        raise NotImplementedError

    def load_data(
        self,
        request,
    ):
        raise NotImplementedError

    def save_changes(
        self,
        request,
        changes,
    ):
        raise NotImplementedError

    def build(
        self,
        request,
    ):
        ctx = MatrixContext(

            matrix=self,

            request=request,

        )

        for step in BUILD_PIPELINE:

            step(
                ctx,
            )

        schema = ctx.schema or {}

        data = ctx.data or {}

        cells = {}

        for item in data.get(
            "items",
            [],
        ):

            row = str(
                item["row"],
            )

            column = str(
                item["column"],
            )

            cells[
                f"{row}:{column}"
            ] = {

                "value":
                    item.get(
                        "value",
                    ),

            }

        layout_rows = schema.get(
            "layoutRows",
            schema.get(
                "rows",
                [],
            ),
        )

        layout_columns = schema.get(
            "layoutColumns",
            schema.get(
                "columns",
                [],
            ),
        )

        return {

            "meta": {

                "type":
                    self.code,

            },

            "layout": {

                "x": [

                    {

                        "id":
                            str(
                                column["id"],
                            ),

                        "label":
                            column["label"],

                    }

                    for column in layout_columns

                ],

                "y": [

                    {

                        "id":
                            str(
                                row["id"],
                            ),

                        "label":
                            row["label"],

                    }

                    for row in layout_rows

                ],

            },

            "cells":
                cells,

            "schema": {

                "defaultCell":

                    schema.get(
                        "defaultCell",
                    ),

                "cells":

                    schema.get(
                        "cells",
                        {},
                    ),

                "columns":

                    schema.get(
                        "columnSchema",
                        {},
                    ),

                "rows":

                    schema.get(
                        "rowSchema",
                        {},
                    ),

            },

            "capabilities":
                ctx.capabilities,

        }

    def submit(
        self,
        request,
        payload,
    ):
        request._matrix_context = (

            payload.get(
                "context",
            )

            or

            payload.get(
                "ctx",
            )

            or

            {}

        )

        ctx = MatrixContext(

            matrix=self,

            request=request,

            payload=payload,

        )

        for step in SUBMIT_PIPELINE:

            step(
                ctx,
            )

        return ctx.result