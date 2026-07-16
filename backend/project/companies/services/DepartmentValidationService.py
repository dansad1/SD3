from django.core.exceptions import (
    ValidationError,
)


class DepartmentValidationService:

    @classmethod
    def validate(
        cls,
        payload,
        instance=None,
    ):

        errors = {}

        cls.validate_name(
            payload,
            errors,
        )

        cls.validate_parent(
            payload,
            instance,
            errors,
        )

        if errors:
            raise ValidationError(
                errors,
            )

        return payload

    # =====================================================
    # NAME
    # =====================================================

    @staticmethod
    def validate_name(
        payload,
        errors,
    ):

        name = payload.get(
            "name",
        )

        if isinstance(
            name,
            str,
        ):
            name = name.strip()

        if not name:

            errors["name"] = [
                "Название обязательно",
            ]

    # =====================================================
    # PARENT
    # =====================================================

    @staticmethod
    def validate_parent(
        payload,
        instance,
        errors,
    ):

        if not instance:
            return

        parent = payload.get(
            "parent",
        )

        if not parent:
            return

        parent_id = getattr(
            parent,
            "pk",
            parent,
        )

        if str(parent_id) == str(instance.pk):

            errors["parent"] = [
                "Отдел не может быть родителем самому себе",
            ]