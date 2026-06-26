from backend.engine.list.BaseList import (
    BaseList,
)

from backend.engine.schema.builder import (
    EntitySchemaBuilder,
)


class AutoEntityList(BaseList):

    def __init__(
            self,
            entity,
    ):

        self.entity = entity

        self.code = (

            f"{entity.entity}.list"

        )

    # =====================================================
    # LIST FIELDS
    # =====================================================

    def get_fields(
            self,
            request,
    ):

        builder = (

            EntitySchemaBuilder(

                self.get_entity(),

            )

        )

        schema = builder.build(

            request,

        )

        entity = (

            self.get_entity()

        )

        allowed = set(

            entity.list_display

            or []

        )

        return [

            {

                "key":

                    field["name"],


                "label":

                    field["label"],


                "sortable":

                    True,

            }

            for field

            in schema["fields"]

            if (

                not allowed

                or

                field["name"]

                in allowed

            )

        ]

    # =====================================================
    # FILTER FIELDS
    # =====================================================

    def get_filter_fields(
            self,
            request,
    ):

        builder = EntitySchemaBuilder(
            self.get_entity(),
        )

        schema = builder.build(
            request,
            action="edit",
        )

        runtime_fields = {
            field.name: field
            for field in self.get_entity().get_fields(
                request,
            )
        }

        result = []

        for field_schema in schema["fields"]:

            runtime = runtime_fields.get(
                field_schema["name"],
            )

            if not runtime:
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

        fields = (

            self.get_fields(

                request,

            )

        )

        return [

            field["key"]

            for field

            in fields

        ]