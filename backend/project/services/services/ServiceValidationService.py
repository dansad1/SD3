from django.core.exceptions import (
    ValidationError,
)

from backend.project.services.models import (
    Service,
)


class ServiceValidationService:

    @classmethod
    def validate(
        cls,
        payload,
        instance=None,
    ):
        errors = {}

        cls.validate_name(
            payload=payload,
            errors=errors,
        )

        cls.validate_code(
            payload=payload,
            instance=instance,
            errors=errors,
        )

        cls.validate_parent(
            payload=payload,
            instance=instance,
            errors=errors,
        )

        if errors:
            raise ValidationError(
                errors,
            )

        return payload

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

    @staticmethod
    def validate_code(
        payload,
        instance,
        errors,
    ):
        code = payload.get(
            "code",
        )

        if isinstance(
            code,
            str,
        ):
            code = code.strip()

        if not code:
            errors["code"] = [
                "Код обязателен",
            ]
            return

        queryset = Service.objects.filter(
            code=code,
        )

        if instance and instance.pk:
            queryset = queryset.exclude(
                pk=instance.pk,
            )

        if queryset.exists():
            errors["code"] = [
                "Сервис с таким кодом уже существует",
            ]

    @staticmethod
    def validate_parent(
        payload,
        instance,
        errors,
    ):
        if not instance or not instance.pk:
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
                "Сервис не может быть родителем самому себе",
            ]