from django.core.exceptions import (
    ValidationError,
)


class WorkScheduleValidationService:

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

        cls.validate_time(
            payload=payload,
            errors=errors,
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
    # TIME
    # =====================================================

    @staticmethod
    def validate_time(
        payload,
        errors,
    ):
        start_time = payload.get(
            "start_time",
        )

        end_time = payload.get(
            "end_time",
        )

        if (
            start_time
            and end_time
            and start_time >= end_time
        ):
            errors["end_time"] = [
                "Время окончания должно быть больше времени начала",
            ]