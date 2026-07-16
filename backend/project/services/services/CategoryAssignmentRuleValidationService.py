from django.core.exceptions import (
    ValidationError,
)

from backend.project.services.models import (
    CategoryAssignmentRule,
)


class CategoryAssignmentRuleValidationService:

    @classmethod
    def validate(
        cls,
        payload,
        instance=None,
    ):
        errors = {}

        service = payload.get(
            "service",
        )

        category = payload.get(
            "category",
        )

        cls.validate_required(
            service=service,
            category=category,
            errors=errors,
        )

        cls.validate_unique(
            service=service,
            category=category,
            instance=instance,
            errors=errors,
        )

        if errors:
            raise ValidationError(
                errors,
            )

        return payload

    # =====================================================
    # REQUIRED
    # =====================================================

    @staticmethod
    def validate_required(
        service,
        category,
        errors,
    ):
        if not service:
            errors["service"] = [
                "Сервис обязателен",
            ]

        if not category:
            errors["category"] = [
                "Категория обязательна",
            ]

    # =====================================================
    # UNIQUE
    # =====================================================

    @staticmethod
    def validate_unique(
        service,
        category,
        instance,
        errors,
    ):
        if (
            not service
            or not category
        ):
            return

        queryset = (
            CategoryAssignmentRule.objects
            .filter(
                service=service,
                category=category,
            )
        )

        if instance and instance.pk:
            queryset = queryset.exclude(
                pk=instance.pk,
            )

        if queryset.exists():
            errors["category"] = [
                "Правило для этой категории уже существует",
            ]