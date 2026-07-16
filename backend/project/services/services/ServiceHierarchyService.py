from django.core.exceptions import (
    ValidationError,
)


class ServiceHierarchyService:

    @classmethod
    def before_save(
        cls,
        ctx,
    ):
        instance = ctx.instance

        parent = ctx.data.get(
            "parent",
        )

        cls.validate_cycle(
            instance=instance,
            parent=parent,
        )

        return ctx

    @staticmethod
    def validate_cycle(
        instance,
        parent,
    ):
        if (
            not instance
            or not instance.pk
            or not parent
        ):
            return

        current = parent
        visited = set()

        while current:
            current_id = current.pk

            if current_id == instance.pk:
                raise ValidationError({
                    "parent": [
                        "Нельзя создать циклическую иерархию",
                    ],
                })

            if current_id in visited:
                raise ValidationError({
                    "parent": [
                        (
                            "В существующей иерархии "
                            "сервисов обнаружен цикл"
                        ),
                    ],
                })

            visited.add(
                current_id,
            )

            current = current.parent

    @classmethod
    def serialize_meta(
        cls,
        obj,
    ):
        return {
            "_depth": cls.get_depth(
                obj,
            ),
            "_parent": obj.parent_id,
            "_has_children": obj.has_children,
        }

    @staticmethod
    def get_depth(
        obj,
    ):
        depth = 0
        parent = obj.parent
        visited = set()

        while parent:
            parent_id = parent.pk

            if parent_id in visited:
                break

            visited.add(
                parent_id,
            )

            depth += 1
            parent = parent.parent

        return depth