from collections import (
    OrderedDict,
)

from backend.project.users.models import (
    Permission,
)


class UserRoleSchemaService:

    @classmethod
    def customize(
        cls,
        request,
        schema,
        field=None,
    ):
        if schema.get(
            "name",
        ) != "permissions":
            return schema

        groups = OrderedDict()

        permissions = (
            Permission.objects
            .all()
            .order_by(
                "category",
                "code",
            )
        )

        for permission in permissions:

            category = (
                permission.category
                or "Общее"
            )

            group = groups.setdefault(
                category,
                {
                    "name": category,
                    "permissions": [],
                },
            )

            group["permissions"].append({
                "id": permission.pk,
                "value": permission.pk,
                "code": permission.code,
                "label": (
                    permission.name
                    or permission.code
                ),
                "description": permission.description,
            })

        schema.update({

            "widget":
                "permission_editor",

            "groups":
                list(
                    groups.values()
                ),

        })

        return schema