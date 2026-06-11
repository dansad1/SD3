from django.core.exceptions import (
    PermissionDenied,
)

import json


class EntitySchemaBuilder:

    def __init__(self, entity):

        self.entity = entity
        self.model = entity.model

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        request,
        action="view",
    ):

        if action not in (
            "view",
            "create",
            "edit",
        ):
            raise PermissionDenied

        self.entity.check_permission(
            request,
            action,
        )

        fields = (
            self.entity.get_fields(
                request
            )
            or []
        )

        fields_schema = []

        seen = set()

        for field in fields:

            if not field.name:
                continue

            if field.name in seen:
                continue

            seen.add(
                field.name
            )

            schema = field.get_schema()

            # =========================================
            # DEBUG
            # =========================================

            print(
                "\n🔍 FIELD SCHEMA"
            )

            print(
                json.dumps(
                    schema,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            )

            if action == "view":
                schema["readonly"] = True

            fields_schema.append(
                schema
            )

        response = {

            "entity":
                self.entity.entity,

            "model":
                self.model.__name__,

            "fields":
                fields_schema,

            "capabilities":
                (
                    self.entity
                    .get_capabilities_for_user(
                        request
                    )
                ),
        }

        print(
            "\n🚀 FINAL FORM SCHEMA"
        )

        print(
            json.dumps(
                response,
                indent=2,
                ensure_ascii=False,
                default=str,
            )
        )

        return response