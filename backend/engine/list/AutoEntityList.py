from backend.engine.list.BaseList import (
    BaseList,
)

from backend.engine.schema.builder import (
    EntitySchemaBuilder,
)


class AutoEntityList(
    BaseList,
):

    def __init__(
        self,
        entity,
    ):

        self.entity = entity

        self.code = (
            f"{entity.entity}.list"
        )

    # =====================================================
    # RUNTIME
    # =====================================================

    def get_runtime_fields(
        self,
        request,
    ):

        return (

            self.get_entity()

            .get_fields(
                request=request,
            )

            or []

        )

    # =====================================================
    # LIST FIELDS
    # =====================================================

    def get_fields(
        self,
        request,
    ):

        runtime_fields = (
            self.get_runtime_fields(
                request,
            )
        )

        builder = EntitySchemaBuilder(
            self.get_entity(),
        )

        schema = builder.build(
            request=request,
            action="view",
            fields=runtime_fields,
        )

        entity = self.get_entity()

        allowed = set(
            entity.list_display
            or []
        )

        result = []

        for field in schema["fields"]:

            if (
                allowed
                and field["name"] not in allowed
            ):
                continue

            result.append({

                "key":
                    field["name"],

                "label":
                    field["label"],

                "sortable":
                    field.get(
                        "sortable",
                        True,
                    ),

            })

        return result

    # =====================================================
    # FILTER FIELDS
    # =====================================================

    def get_filter_fields(
        self,
        request,
    ):

        runtime_fields = (
            self.get_runtime_fields(
                request,
            )
        )

        builder = EntitySchemaBuilder(
            self.get_entity(),
        )

        schema = builder.build(
            request=request,
            action="edit",
            fields=runtime_fields,
        )

        runtime_map = {

            field.name: field

            for field in runtime_fields

        }

        result = []

        for field_schema in schema["fields"]:

            runtime = runtime_map.get(
                field_schema["name"],
            )

            if runtime is None:
                continue

            if not runtime.field_type.filterable:
                continue

            field_schema.pop(
                "readonly",
                None,
            )

            result.append(
                field_schema,
            )

        return result

    # =====================================================
    # DEFAULT VISIBLE
    # =====================================================

    def get_default_visible_fields(
        self,
        request,
    ):

        return [

            field["key"]

            for field in self.get_fields(
                request,
            )

        ]